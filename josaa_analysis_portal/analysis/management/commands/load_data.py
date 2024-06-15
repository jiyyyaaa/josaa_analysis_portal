import csv
import os
from django.core.management.base import BaseCommand
from analysis.models import rank_data

class Command(BaseCommand):
    help = 'Load data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the CSV file to be loaded',
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        if not os.path.isfile(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                opening_rank = int(float(row['Opening Rank']))
                closing_rank = int(float(row['Closing Rank']))

                rank_data.objects.create(
                    institute=row['Institute'],
                    program=row['Academic Program Name'],
                    seat_type=row['Seat Type'],
                    gender=row['Gender'],
                    opening_rank=opening_rank,
                    closing_rank=closing_rank,
                    year=int(row['Year']),
                    roundNo=int(row['Round'])
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded data from {file_path}'))
