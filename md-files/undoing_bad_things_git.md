<!--date 05.08.2018-->
<!--title Правка изменений в Git-->
<!--meta_description Будем говорить о том, как в Git изменить последний коммит, вернуться к какому-то коммиту назад, откатить изменения в файле, а также перенести коммиты из одной ветки в другую.-->


В Git часто бывает нужно исправить последствия неправильно выполненных действий.
Например, изменить последний коммит, вернуться к какому-то моменту назад или перенести коммиты из одной ветки в другую.

Рассмотрим, как это можно делать.

## git checkout filename
Эта команда возвращает файл к состоянию последнего коммита

## git commit --amend
Пусть в последний коммит не вошли какие-то файлы или сообщение коммита оказалось
неверным. Тогда можно добавить/удалить необходимые файлы и выполнить `git commit --amend`. Эта команда внесет необходимые изменения, да еще позволит изменить текст
сообщения коммита.

## git cherry-pick hash1 hash2 ...
Пусть мы делали изменения не в той ветке, в которой хотели. Тогда нужно перейти в ветку назначения и выполнить `git cherry-pick` для переноса коммитов по их хэшам.

## git reset (--soft, --mixed, --hard) hash
`--soft` - все изменения с коммита hash будут добавлены в Staging Area (как с помощью git add)

`--mixed` - значение по умолчанию, все изменения будут отображаться как не добавленные в Staging Area

`--hard` - будет все, как в коммите hash, только новые файлы буду отображаться как Untracked. Чтобы избавиться от них нужно выполнить `git clean -df`.

## git revert hash1 hash2 ...
Данная команда создает коммит, обращающий коммит hash1. Затем создает коммит, обращающий коммит hash2 и т.д.
Это единственная безопасная команда, меняющая историю, которая уже есть в remote.


*Для более полного ознакомления со всеми этими командами есть [видео на Youtube](https://youtu.be/FdZecVxzJbk)*