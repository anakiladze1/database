import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('students.database.sqlite3')
cursor = conn.cursor()

df = pd.read_sql_query("SELECT * FROM students", conn)
# დაბეჭდავს მხოლოდ მდედრობითი სქესის წარმომადგენლებს
cursor.execute("SELECT * FROM students WHERE gender = ?", ("female",))
rows = cursor.fetchall()
print("ქალი სტუდენტის სია:")
for row in rows:
    print(row)

# ახალი ჩანაწერის დამატება
gender = input("შეიყვანეთ სქესი: ")
ethnicity = input("შეიყვანეთ ეთნიკური ჯგუფი: ")
parental_education = input("მშობლის განათლება: ")
lunch = input("ლანჩის ტიპი: ")
test_prep = input("ტესტის მომზადება (completed/none): ")
math_score = int(input("მათემატიკის ქულა: "))
reading_score = int(input("კითხვის ქულა: "))
writing_score = int(input("წერის ქულა: "))

cursor.execute("""
    INSERT INTO students (gender, ethnicity, parental_level_of_education, lunch, test_preparation_course, math_score, reading_score, writing_score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (gender, ethnicity, parental_education, lunch, test_prep, math_score, reading_score, writing_score))

conn.commit()

#აქ რაც დავამატე მაგას ვამოწმებ და ვაბეჭდინებ ხომ სწორადაა
cursor.execute("SELECT rowid, * FROM students ORDER BY rowid DESC LIMIT 1")
last_row = cursor.fetchone()
print("ბოლოს დამატებული სტუდენტი:")
print(last_row)



# განახლდება მათემატიკის ქულა  rowid-ის მიხედვით
record_id = int(input("შეიყვანეთ ჩანაწერის ID განახლებისთვის: "))
new_math_score = int(input("შეიყვანეთ ახალი მათემატიკის ქულა: "))

cursor.execute("""
    UPDATE students SET math_score = ? WHERE rowid = ?
""", (new_math_score, record_id))

conn.commit()

# შლის ჩანაწერს მითითებული rowid-ის მიხედვით

record_id = int(input("შეიყვანეთ ჩანაწერის ID წასაშლელად: "))

cursor.execute("DELETE FROM students WHERE rowid = ?", (record_id,))

conn.commit()

#ბოლოს კიდევ ვაბეჭდინებ და ვნახულობს რომ ყველაფერი სწორედ განახდა, წაიშალა და დაემატა
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
for row in rows:
    print(row)




# დიაგრამები


# მათემატიკის ქულების განაწილება  სტუდენტთა რაოდენობის მიხედვით
math_scores = df['math_score']
plt.hist(math_scores, bins=10, color='skyblue')
plt.title('მათემატიკის ქულების განაწილება')
plt.xlabel('ქულა')
plt.ylabel('სტუდენტების რაოდენობა')
plt.show()

#ეთნიკური ჯგუფების პროცენტული გადანაწილება
ethnicity_counts = df['ethnicity'].value_counts()
plt.pie(ethnicity_counts, labels=ethnicity_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('ეთნიკური ჯგუფების პროცენტული განაწილება')
plt.show()



plt.scatter(df['math_score'], df['writing_score'], alpha=0.6)
plt.title('მითემატიკის და წერის ქულების ურთიერთკავშირი')
plt.xlabel('მითემატიკის ქულა')
plt.ylabel('წერის ქულა')
plt.show()

conn.close()

