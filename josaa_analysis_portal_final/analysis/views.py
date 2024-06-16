from django.shortcuts import render
from .forms import RankForm, RankDifferenceForm
from .models import rank_data
from collections import defaultdict
from django.db.models import Avg
from django.http import JsonResponse
import json
import random


def index(request):
    return render(request, 'analysis/index.html')

def result_page(request):
    form = RankForm(request.POST or None)
    results = {}

    if request.method == 'POST':
        if form.is_valid():
            rank = form.cleaned_data['rank']
            gender = form.cleaned_data['gender']
            seat_type = form.cleaned_data['seat_type']

            colleges = rank_data.objects.filter(
                gender=gender,
                seat_type=seat_type,
                closing_rank__gte=rank
            ).values('institute').distinct().order_by('institute')

            for college in colleges:
                programs = rank_data.objects.filter(
                    gender=gender,
                    seat_type=seat_type,
                    institute=college['institute'],
                    closing_rank__gte=rank
                ).values('program').distinct().order_by('program')

                results[college['institute']] = []

                for program in programs:
                    years = rank_data.objects.filter(
                        gender=gender,
                        seat_type=seat_type,
                        institute=college['institute'],
                        program=program['program'],
                        closing_rank__gte=rank
                    ).values_list('year', flat=True).distinct().order_by('year')

                    if years:
                        results[college['institute']].append({
                            'program': program['program'],
                            'years': years
                        })

    context = {
        'form': form,
        'results': results
    }
    return render(request, 'analysis/result.html', context)

def popularity_chart(request):
    colleges = rank_data.objects.values('institute').distinct()

    if request.method == 'POST':
        college_name = request.POST.get('college_name')

        if college_name:
            # Get distinct programs for the selected college
            programs = rank_data.objects.filter(institute=college_name, seat_type='OPEN').values('program').distinct()

            # Prepare data for each program
            datasets = []
            labels_set = set()

            for program in programs:
                # Aggregate data to calculate average opening rank for each year
                year_data = rank_data.objects.filter(institute=college_name, program=program['program'], seat_type='OPEN') \
                                             .values('year') \
                                             .annotate(avg_opening_rank=Avg('opening_rank')) \
                                             .order_by('year')

                # Debug: Print the year data for this program
                print(f"Program: {program['program']}, Year Data: {list(year_data)}")

                # Extract labels (years) and data (avg opening ranks)
                labels = [entry['year'] for entry in year_data]
                data = [entry['avg_opening_rank'] for entry in year_data]

                labels_set.update(labels)

                datasets.append({
                    'label': program['program'],
                    'data': data,
                    'borderColor': f'rgba({random_color()}, 1)',  # Customize as needed
                })

            chart_data = {
                'labels': sorted(labels_set),  # Assuming all programs have the same years
                'datasets': datasets
            }

            return render(request, 'analysis/popularity_chart.html', {'chart_data': json.dumps(chart_data), 'colleges': colleges})

    # Handle case where no institute is selected or initial GET request
        return render(request, 'analysis/popularity_chart.html', {'colleges': colleges})

    else:
        # Handle GET request or any other request method
        return render(request, 'analysis/popularity_chart.html', {'colleges': rank_data.objects.values('institute').distinct()})

# Function to generate random RGB color values
def random_color():
    import random
    return f"{random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}"


def iit_branches(request):
    # Retrieve all unique institutes (IITs)
    institutes = rank_data.objects.values_list('institute', flat=True).distinct()
    institutes= institutes.exclude(institute='Indian School of Mines Dhanbad')
    # Create a list to store each IIT with its programs
    colleges = []

    # Iterate over each institute to fetch its programs
    for institute in institutes:
        programs = rank_data.objects.filter(institute=institute).values('program').distinct()

        # Append the institute and its programs to the colleges list
        colleges.append({
            'institute': institute,
            'branches': programs
        })

    # Render the template with the colleges data
    return render(request, 'analysis/iit_branches.html', {'colleges': colleges})