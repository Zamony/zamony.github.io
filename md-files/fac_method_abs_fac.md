<!--date 31.01.2018-->
<!--title Simple Factory, Factory Method и Abstract Factory-->
<!--meta_description Паттерны проектирования Simple Factory, Factory Method и Abstract Factory часто путают между собой. Рассмотрим отличия и особенности применения каждого из них.-->

Simple Factory, Factory Method и Abstract Factory - это паттерны 
проектирования, то есть решения каких-то конкретных проблем проектирования 
программ.

> Все рассказы серии:
> * Simple Factory, Factory Method и Abstract Factory
> * [Decorator](/pages/decorator)

И Simple Factory, и Factory Method, и Abstract Factory относятся к порождающим 
паттернам, то есть к паттернам, отвечающим за создание объектов.

Первым мы рассмотрим паттерн Simple Factory, так как он самый простой и поможет
понять нам другие паттерны этой статьи.

## Simple Factory
Пусть у нас есть игра, в которой есть монстры-вампиры и они могут сражаться с
главным героем. Тогда код нашей игры будет выглядеть как-то так:
```cpp
struct Vampire {
    void fight(){
        std::cout << "Vampire is fighting" << std::endl;
    }
};

int main(){
    auto monster = Vampire{};
    monster.fight();

    return 0;
}
```
Чем плох этот код?
1. Если мы захотим заменить имя класса `Vampire` на более подходящее, скажем,
`RedVampire` то нам придется делать замену имени во всем коде.
2. Пусть у нас был класс `Vampire{}`, но мы изменили его конструктор и теперь он
принимает аргументом величину здоровья `Vampire{100}`, тогда по всему коду
опять придется искать и менять.

Чтобы показать, что паттерн *Simple Factory* решает эти проблемы, добавим в нашу
игру вервольфов, отнаследовав от общего интерфейса монстров.

```cpp

struct Monster {
    virtual void fight() = 0;
};
struct Vampire : Monster{
    void fight(){
        std::cout << "Vampire is fighting" << std::endl;
    }
};
struct Werewolf : Monster{
    void fight(){
        std::cout << "Werewolf is fighting" << std::endl;
    }
};
```
Итак, о самом паттерне. **Паттерн Simple Factory** определяет класс, в котором
есть метод создающий объекты разного типа в зависимости от аргумента этого
метода.

```cpp
struct MonsterFactory {
    std::unique_ptr<Monster> createMonster(std::string monster_type){
        if (monster_type == "vampire")
            return std::make_unique<Vampire>();
        else if (monster_type == "werewolf")
            return std::make_unique<Werewolf>();
        return nullptr;
    }
};

int main(){
    MonsterFactory monster_factory;
    auto monster = monster_factory.createMonster("werewolf");
    if (monster != nullptr){
        monster->fight();
    }

    return 0;
}
```
Выше были указаны две проблемы, которые возникают при непосредственном создании
объектов классов. Посмотрим, как они были разрешены при использовании паттерна
Simple Factory:
1. Как можно видеть, если мы изменим имя класса `Vampire` на более подходящее
`RedVampire`, то нам нужно будет изменить всего одну строчку в createMonster()
2. То же самое и с конструктором
3. *Как бонус* мы получили возможность выбора класса для создания объекта во
время работы программы. Например, мы могли попросить пользователя ввести, какого
монстра создать, или сделать выбор случайным  образом.

## Factory Method
Но у паттерна Simple Factory есть и большой недостаток: он нарушает [принцип
открытости/закрытости](https://ru.wikipedia.org/wiki/Принцип_открытости/закрытости).

Когда мы добавляли поддержку класса Werewolf в программу, то изменяли логику
работы старого кода. На месте нашего игрушечного примера могло бы быть что-то
более сложное - объекты классов бы порождались совсем нетривиально. И что-то
могло бы сломаться. Это и есть нарушение принципа открытости/закрытости.

Нам нужно добавлять функциональность в виде классов, что и предлагает делать
паттерн Factory Method.

```cpp
struct Monster {
    virtual void fight() = 0;
};
struct Vampire : Monster{
    void fight(){
        std::cout << "Vampire is fighting" << std::endl;
    }
};
struct Werewolf : Monster{
    void fight(){
        std::cout << "Werewolf is fighting" << std::endl;
    }
};

struct MonsterFactory {
    virtual std::unique_ptr<Monster> createMonster() = 0;
};

struct VampireFactory : MonsterFactory {
    virtual std::unique_ptr<Monster> createMonster(){
        return std::make_unique<Vampire>();
    }
};

struct WerewolfFactory : MonsterFactory {
    virtual std::unique_ptr<Monster> createMonster(){
        return std::make_unique<Werewolf>();
    }
};

int main(){
    auto factory = WerewolfFactory{};
    auto monster = factory.createMonster();
    monster->fight();

    return 0;
}
```

## Abstract Factory
Abstract Factory - это почти фабричный метод. Только здесь классы Factory
имеют несколько методов создания объектов, а не один.

Зачем это может быть нужно? Это может быть нужно, если мы хотим порождать
объекты как-то связанные между собой, *объекты одной группы*. 
Поэтому порождающие их методы и выносят в одну фабрику.

Для нашего примера с монстрами трудно придумать использование Abstract Factory,
поэтому разберем новый пример.

Пусть у нас есть графическое приложение, которое должно работать и в Windows, и
в MacOS. Эти операционные системы совершенно разные, значит коды отрисовки
кнопок и текстовых полей тоже будут различаться.

Имеем классы кнопок и текстовых полей объявленные как:

```cpp
struct Button {
    virtual void draw() = 0;
};
struct WindowsButton : Button {
    void draw(){
        std::cout << "Rendering Windows button" << std::endl;
    }
};
struct MacOSButton : Button {
    void draw(){
        std::cout << "Rendering MacOS button" << std::endl;
    }
};

struct TextBox {
    virtual void draw() = 0;
};
struct WindowsTextBox : TextBox {
    void draw(){
        std::cout << "Rendering Windows textbox" << std::endl;
    }
};
struct MacOSTextBox : TextBox {
    void draw(){
        std::cout << "Rendering MacOS textbox" << std::endl;
    }
};
```

Тогда пусть WindowsGUIFactory производит кнопки и текстовые поля для Windows, а
MacOSGUIFactory производит кнопки и текстовые поля для MacOS:

```cpp
struct GUIFactory {
    virtual std::unique_ptr<Button> createButton() = 0;
    virtual std::unique_ptr<TextBox> createTextBox() = 0;
};
struct WindowsGUIFactory : GUIFactory {
    std::unique_ptr<Button> createButton(){
        return std::make_unique<WindowsButton>();
    }
    std::unique_ptr<TextBox> createTextBox(){
        return std::make_unique<WindowsTextBox>();
    }
};
struct MacOSGUIFactory : GUIFactory {
    std::unique_ptr<Button> createButton(){
        return std::make_unique<MacOSButton>();
    }
    std::unique_ptr<TextBox> createTextBox(){
        return std::make_unique<MacOSTextBox>();
    }
};

int main(){
    auto factory = std::make_unique<MacOSGUIFactory>();
    auto button = factory->createButton();
    auto textbox = factory->createTextBox();

    button->draw();
    textbox->draw();

    return 0;
}
```
Получили все те же плюсы паттерна Factory Method, только здесь мы подчеркиваем
связность группы порождаемых объектов.