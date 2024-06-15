# views.py

from django.shortcuts import render
from .forms import RankForm
from .models import rank_data
from collections import defaultdict
import pprint
from collections import defaultdict
from django.db.models import Min, Max
from django.db import models

def index(request):
    return render(request, 'analysis/index.html')

def input_form(request):
    form = RankForm()
    return render(request, 'analysis/input_form.html', {'form': form})

def process_form(request):
    if request.method == 'POST':
        form = RankForm(request.POST)
        if form.is_valid():
            rank = form.cleaned_data['rank']
            gender = form.cleaned_data['gender']
            seat_type = form.cleaned_data['seat_type']

            # Fetch colleges with their associated programs
            colleges = rank_data.objects.filter(
                gender=gender,
                seat_type=seat_type,
                opening_rank__lte=rank,
                closing_rank__gte=rank
            ).values('institute').distinct()

            results = {}

            for college in colleges:
                # Get the programs for each college
                programs = rank_data.objects.filter(
                    gender=gender,
                    seat_type=seat_type,
                    institute=college['institute']
                ).values('program').distinct()

                program_list = []

                for program in programs:
                    # Get years and their opening and closing ranks for each program
                    years_data = rank_data.objects.filter(
                        gender=gender,
                        seat_type=seat_type,
                        institute=college['institute'],
                        program=program['program']
                    ).values('year').annotate(
                        min_opening_rank=models.Min('opening_rank'),
                        max_closing_rank=models.Max('closing_rank')
                    ).order_by('year')

                    program_info = {
                        'program_name': program['program'],
                        'years': list(years_data)
                    }

                    program_list.append(program_info)

                results[college['institute']] = program_list

            context = {
                'results': results
            }
            return render(request, 'analysis/result.html', context)

    # Handle GET request or invalid form case
    else:
        form = RankForm()

    return render(request, 'analysis/input_form.html', {'form': form})