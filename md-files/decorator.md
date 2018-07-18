<!--date 28.03.2018-->
<!--title Паттерн Decorator-->
<!--meta_description Паттерн декоратор - это мощный паттерн проектирования, который представляет собой альтернативу наследованию. Рассмотрим применение и различные вариации паттерна-->

Паттерн Decorator - это структурный паттерн проектирования.
Структурные паттерны компонуют объекты вместе, чтобы получить более
гибкую архитектуру.

> Все рассказы серии:
> * [Simple Factory, Factory Method и Abstract Factory](/pages/simple-factory-factory-method-i-abstract-factory)
> * Decorator

## Мотивация использования
Мы будем разбирать паттерн Decorator на примере игры, в которой главный
герой на клеточной доске сражается с монстрами.

![Пример игры](/imgs/board_game2.png)

При этом возможно следующее:
* главный герой может заморозить противника, чтобы тот не смог переместиться в другую клетку
* противник может перейти в состояние ярости, тогда наносимый им урон увеличиться

Первое решение, которое может придти в голову - это для каждого конкретного
монстра в игре выделить класс, а от него отнаследовать все возвможные
классы-состояния:


![Пример плохой реализации, нужен декоратор](/imgs/decorator_bad_example.png)


Но в будущем у нас могут добавиться новые типы монстров и новые возможности в
игре (например, отравление, воспламенение и др.). Тогда число классов, которые
нам нужно будет создавать, будет очень велико. Поддерживать такую игру будет 
сложно.

### Первая версия Decorator
![Паттерн декоратор, можно улучшить](/imgs/decorator_not_bad.png)

Что, если перенести состояния заморозки и ярости
(а они меняют функции объекта-моснтра) с каждого конкретного монстра, на всех
монстров в целом? То есть создать класс заморозки, и в его конструктор
передавать конкретного монстра, и у нас был бы замороженный монстр
(замороженный монстр является монстром, поэтому класс заморозки должен быть
отнаследован от `IMonster`).

Такой подход решил бы вопросы с поддерживаемостью, так как не пришлось бы для каждого
монстра порождать кучу подклассов.

```cpp
#include <iostream>
#include <memory>

struct IMonster {
    virtual void move() = 0;
    virtual void attack(int = 0) = 0;
    virtual ~IMonster(){}
};

struct Dragon : IMonster {
    Dragon(int in_damage): _damage(in_damage){
        std::cout << "Создан монстр - дракон" << std::endl;
    }
    void move(){
        std::cout << "Дракон перемещается в новую клетку" << std::endl;   
    }    
    void attack(int addition = 0){
        std::cout << "Дракон нападает, получен урон - " << _damage + addition
                  << " единиц" << std::endl;
    }
    const int _damage;
};

struct IceIMonsterDecorator : IMonster {
    IceIMonsterDecorator(std::unique_ptr<IMonster> in_monster)
    :_monster(std::move(in_monster)){}
    void move(){
        std::cout << "Заморожен в лед и не может переместиться" << std::endl;
    }
    void attack(int addition = 0){
        _monster->attack(addition);
    }
    private:
    std::unique_ptr<IMonster> _monster;
};

struct InRageIMonsterDecorator : IMonster {
    InRageIMonsterDecorator(std::unique_ptr<IMonster> in_monster)
    :_monster(std::move(in_monster)){}
    void move(){
        _monster->move();
    }
    void attack(int addition = 0){
        std::cout << "Приведен в ярость, будет атаковать на 5 единиц мощнее"
                  << std::endl;
        _monster->attack(addition + 5);
    }
    private:
    std::unique_ptr<IMonster> _monster;
};

int main(){
    std::unique_ptr<IMonster> monster = std::make_unique<IceIMonsterDecorator>(
        std::make_unique<InRageIMonsterDecorator>(
            std::make_unique<Dragon>(25)
        )
    );
    monster->move();
    monster->attack();

    return 0;
}
```
Вывод программы:
```bash
Создан монстр - дракон
Заморожен в лед и не может переместиться
Приведен в ярость, будет атаковать на 5 единиц мощнее
Дракон нападает, получен урон - 30 единиц
```

Но и у этой реализации есть минусы. Декоратор ведь не обязан изменять
функциональность всех методов `IMonster`. Тогда в методах, которые он не
изменяет, идет простое перенаправление вызовов к своему внутреннему объекту.

Только у нас в примере `IMonster` имеет всего два метода, но если бы их было 
много, тогда в каждом классе-декораторе содержалось бы много одинаковых методов
перенаправителей. Это было бы дублированием кода, а где дублирование, там и
ошибки.

### Вторая версия Decorator
Проблема выше решается введением общего класса `IMonsterDecorator`.

![Паттерн декоратор](/imgs/decorator_good.png)

Теперь классы-декораторы могут переопределять только те методы, которые им
нужны, для изменения функциональности объекта.

```cpp
#include <iostream>
#include <memory>

struct IMonster {
    virtual void move() = 0;
    virtual void attack(int = 0) = 0;
    virtual ~IMonster(){}
};

struct Dragon : IMonster {
    Dragon(int in_damage): _damage(in_damage){
        std::cout << "Создан монстр - дракон" << std::endl;
    }
    void move(){
        std::cout << "Дракон перемещается в новую клетку" << std::endl;   
    }    
    void attack(int addition = 0){
        std::cout << "Дракон нападает, получен урон - " << _damage + addition
                  << " единиц" << std::endl;
    }
    const int _damage;
};

struct IMonsterDecorator : IMonster {
    IMonsterDecorator(std::unique_ptr<IMonster> in_monster)
    :_monster(std::move(in_monster)){}
    void move(){
        _monster->move();
    }
    void attack(int addition = 0){
        _monster->attack(addition);
    }    
    private:
    std::unique_ptr<IMonster> _monster;
};

struct IceIMonsterDecorator : IMonsterDecorator {
    IceIMonsterDecorator(std::unique_ptr<IMonster> in_monster)
    :IMonsterDecorator(std::move(in_monster)){}
    void move(){
        std::cout << "Заморожен в лед и не может переместиться" << std::endl;
    }
};

struct InRageIMonsterDecorator : IMonsterDecorator {
    InRageIMonsterDecorator(std::unique_ptr<IMonster> in_monster)
    :IMonsterDecorator(std::move(in_monster)){}
    void attack(int addition = 0){
        std::cout << "Приведен в ярость, будет атаковать на 5 единиц мощнее"
                  << std::endl;
        IMonsterDecorator::attack(addition+5);
    }
};

int main(){
    std::unique_ptr<IMonster> monster = std::make_unique<IceIMonsterDecorator>(
        std::make_unique<InRageIMonsterDecorator>(
            std::make_unique<Dragon>(25)
        )
    );
    monster->move();
    monster->attack();

    return 0;
}
```
### Выводы по паттерну Decorator
**Паттерн Decorator** может использован там, где нужно прямо во время работы
программы навешивать на объект новый функционал.

В нашем примере замороженный дракон не мог переместиться в другую
клетку - мы наделили объект этой функцией уже после его создания, обернув его в
`IceIMonsterDecorator`.