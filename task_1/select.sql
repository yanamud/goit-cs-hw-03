--1. Отримати всі завдання певного користувача. 
--Використайте SELECT для отримання завдань конкретного користувача за його user_id.

select * from tasks where user_id = 4

--2. Вибрати завдання за певним статусом. 
--Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.

select * from tasks where status_id = (select id from status where name = 'new')

--3. Оновити статус конкретного завдання. 
--Змініть статус конкретного завдання на 'in progress' або інший статус.

UPDATE tasks SET status_id = (select id from status where name = 'in progress') 
	WHERE user_id = (select user_id from tasks 
		WHERE status_id = (select id from status where name = 'new') limit 1)

--4. Отримати список користувачів, які не мають жодного завдання. 
--Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
		
select id, fullname from users where id not in 
	(select distinct user_id from tasks order by user_id)

--5. Додати нове завдання для конкретного користувача. 
--Використайте INSERT для додавання нового завдання.
	
INSERT INTO tasks ( title, description, status_id, user_id)  
VALUES ( 'Do homework', 'there are tasks 1-4 to be done',1, 5)

--6. Отримати всі завдання, які ще не завершено. 
--Виберіть завдання, чий статус не є 'завершено'.

select * from tasks where status_id not in (select id from status where name = 'done')

--7. Видалити конкретне завдання. 
--Використайте DELETE для видалення завдання за його id.

DELETE FROM tasks  WHERE id = 10

--8. Знайти користувачів з певною електронною поштою. 
--Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.

select * from users where email like '%.net' and email like 'j%'

--9. Оновити ім'я користувача. 
--Змініть ім'я користувача за допомогою UPDATE.
UPDATE users  SET fullname = 'Emily Snow' where fullname = 'Emily Green'

--10. Отримати кількість завдань для кожного статусу. 
--Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.

select status_id, count(status_id) as total from tasks
group by status_id
order by status_id

--11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
--Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені 
--користувачам, чия електронна пошта містить певний домен (наприклад, '%@example.com').

select * from tasks as t
join
(select id from users where email like '%@example.com' order by id) as u
on u.id = t.user_id 
order by t.id 

--12. Отримати список завдань, що не мають опису. 
--Виберіть завдання, у яких відсутній опис.

INSERT INTO tasks ( title, status_id, user_id)  
VALUES ( 'Do homework',1, 1)

select * from tasks where description is null 

--13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. 
--Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.

select t.user_id, t.title as task, s.name as status from tasks as t
join status as s 
on t.status_id = s.id 
where s."name" = 'in progress'
order by t.user_id

--14. Отримати користувачів та кількість їхніх завдань. 
--Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.

select u.id, u.fullname, t.count_tasks from users as u 
left join 
	(select user_id, count(user_id) as count_tasks from tasks
	group by user_id
	order by user_id) as t
on u.id = t.user_id
order by u.id