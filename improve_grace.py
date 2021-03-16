import random
from django.core.management.base import BaseCommand, CommandError
from datacenter.models import Mark, Schoolkid, Chastisement, \
    Commendation, Lesson


class Command(BaseCommand):
    help = "Улучшает успеваемость"

    def add_arguments(self, parser):
        parser.add_argument(
            'schoolkid_fullname',
            type=str,
            help='Если не указано дополнительных параметров,\
                ищет ученика и исправляет плохие оценки на 5'
        )
        parser.add_argument(
            '--subject',
            type=str,
            help='Добавляет случайную похвалу от учителя \
                к последнему уроку по предмету'
        )

  



    def fix_marks(self, schoolkid):
        return Mark.objects.filter(
            schoolkid=schoolkid,
            points__in=[2, 3]
            ).update(points=5)

    def remove_chastisements(self, schoolkid):
        return Chastisement.objects.filter(
            schoolkid=schoolkid
            ).delete()[0]

    def create_commendation(self):
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

        if not self.last_lesson:
            return None

        commendation, create = Commendation.objects.get_or_create(
            schoolkid=self.schoolkid,
            subject=self.last_lesson.subject,
            created=self.last_lesson.date,
            defaults={
                'text': random.choice(commendations),
                'teacher': self.last_lesson.teacher
            }
        )

        return commendation.text

    def handle(self, *args, **options):
        schoolkids_fullname = options['schoolkid_fullname']

        try:
            self.schoolkid = Schoolkid.objects.get(
                full_name__contains=schoolkids_fullname
            )
        except Schoolkid.DoesNotExist:
            raise CommandError(f'Ученика {schoolkids_fullname} не найдено')
        except Schoolkid.MultipleObjectsReturned:
            found_schoolkids = Schoolkid.objects.filter(
                full_name__contains=schoolkids_fullname
            )
            raise CommandError(
                f'Найдено несколько учеников с именем {schoolkids_fullname}: \
                     {found_schoolkids}'
            )

        self.stdout.write(self.style.SUCCESS(
            f'Исправлено {self.fix_marks(self.schoolkid)} оценок'))
        self.stdout.write(self.style.SUCCESS(
            f'Удалено {self.remove_chastisements(self.schoolkid)} замечаний'))

        if options['subject']:
            self.last_lesson = Lesson.objects.filter(
                year_of_study=self.schoolkid.year_of_study,
                group_letter=self.schoolkid.group_letter,
                subject__title__contains=options['subject']
            ).order_by('-date').first()
            success_output = self.style.SUCCESS(
                'Учитель {teacher} похвалил {schoolkid}: {commendation}'
            )
            negative_output = self.style.WARNING('Предмет не найден')
            output = negative_output if not self.last_lesson else success_output.format(
                teacher=self.last_lesson.teacher,
                schoolkid=self.schoolkid,
                commendation=self.create_commendation()
            )
            print(output)
            
