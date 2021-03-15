from django.core.management.base import BaseCommand, CommandError
from datacenter.models import Mark, Schoolkid, Chastisement, Commendation, Lesson
import random



class Command(BaseCommand):
    help = "Улучшает успеваемость"

    def add_arguments(self, parser):
        parser.add_argument('schoolkid_fullname', type=str, help='Если не указано дополнительных параметров, ищет ученика и исправляет плохие оценки на 5')
        parser.add_argument('--subject', type=str, help='Добавляет случайную похвалу от учителя к последнему уроку по предмету', )

       
    def fix_marks(self, schoolkid):
        return Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)

    def remove_chastisements(self, schoolkid):
        return Chastisement.objects.filter(schoolkid=schoolkid).delete()
        
    def create_commendation(self, schoolkids_fullname, subject_title):
        commendations = [
            'Молодец!',
            'Отлично!',
            'Хорошо!',
            'Гораздо лучше, чем я ожидал!',
            'Ты меня приятно удивил!',
            'Великолепно!',
            'Прекрасно!',
            'Ты меня очень обрадовал!',
            'Именно этого я давно ждал от тебя!',
            'Сказано здорово – просто и ясно!',
            'Ты, как всегда, точен!',
            'Очень хороший ответ!',
            'Талантливо!',
            'Ты сегодня прыгнул выше головы!',
            'Я поражен!',
            'Уже существенно лучше!',
            'Потрясающе!',
            'Замечательно!',
            'Прекрасное начало!',
            'Так держать!',
            'Ты на верном пути!',
            'Здорово!',
            'Это как раз то, что нужно!',
            'Я тобой горжусь!',
            'С каждым разом у тебя получается всё лучше!',
            'Мы с тобой не зря поработали!',
            'Я вижу, как ты стараешься!',
            'Ты растешь над собой!',
            'Ты многое сделал, я это вижу!',
            'Теперь у тебя точно все получится!'
        ]
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkids_fullname)
        last_lesson = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject__title__contains=subject_title).order_by('-date').first()
        if not last_lesson:
            return
        subject = last_lesson.subject
        text = random.choice(commendations)
        teacher=last_lesson.teacher
        date = last_lesson.date
        return Commendation.objects.create(teacher=teacher, subject=subject, schoolkid=schoolkid, created=date, text=text)

    def handle(self, *args, **options):
        schoolkids_fullname = options['schoolkid_fullname']
        
        try:
            schoolkid = Schoolkid.objects.get(full_name__contains=schoolkids_fullname)
        except Schoolkid.DoesNotExist:
            raise CommandError(f'Ученика {schoolkids_fullname} не найдено')
        except Schoolkid.MultipleObjectsReturned:
            raise CommandError(f'Найдено несколько учеников с именем {schoolkids_fullname}: {Schoolkid.objects.filter(full_name__contains=schoolkids_fullname)}') 
        
        self.stdout.write(self.style.SUCCESS(f'Исправлено {self.fix_marks(schoolkid)} оценок'))
        self.stdout.write(self.style.SUCCESS(f'Удалено {self.remove_chastisements(schoolkid)} замечаний'))

        if options['subject']:
            subject = options['subject']
            commendation = self.create_commendation(schoolkids_fullname, subject)
            result = self.style.SUCCESS(f'Учитель {commendation.teacher} похвалил {commendation.schoolkid}: {commendation.text}')\
                 if commendation\
                 else self.style.WARNING('Предмет не найден')
            self.stdout.write(self.style.WARNING(result))
