from bs4 import BeautifulSoup


# Read-only file
with open('home.html', 'r') as file:
    file_content = file.read()
    soup = BeautifulSoup(file_content, 'lxml')

    course_cards = soup.find_all('div', class_='card')
    for card in course_cards:
        course_name = card.h5.text
        course_price = card.a.text.split()[-1]

        print(f'{course_name} costs {course_price}')
