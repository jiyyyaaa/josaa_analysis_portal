from django.db import models

class rank_data(models.Model):
    institute = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    seat_type = models.CharField(max_length=50)
    gender = models.CharField(max_length=100)
    opening_rank = models.FloatField()  # Change from IntegerField to FloatField
    closing_rank = models.FloatField()  # Change from IntegerField to FloatField
    year = models.IntegerField()
    roundNo = models.IntegerField()

    def __str__(self):
        return (f'Institute: {self.institute}, Program: {self.program}, '
                f'Seat Type: {self.seat_type}, Gender: {self.gender}, '
                f'Opening Rank: {self.opening_rank}, Closing Rank: {self.closing_rank}, '
                f'Year: {self.year}, Round No: {self.roundNo}')