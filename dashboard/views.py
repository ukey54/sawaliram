
from django.shortcuts import render
from django.http import HttpResponse
from dashboard.models import Question
from datetime import datetime
from pprint import pprint
import random
import pandas as pd

""" get_view funcions
They return a view or a page
"""
def get_login_view(request):
	return HttpResponse("Dashboard Login")

def get_home_view(request):
	context = {}
	return render(request, 'dashboard/home.html', context)

def get_submit_questions_view(request):
	return render(request, 'dashboard/submit-questions.html')

def get_submit_excel_sheet_view(request):

	context = {
		'excel_file_name': 'excel' + str(random.randint(1, 999)),
	}

	return render(request, 'dashboard/submit-excel-sheet.html', context)

def get_view_questions_view(request):
	return HttpResponse("View Questions here!")

def get_error_404_view(request, exception):
	return render(request, 'dashboard/404.html')

def get_work_in_progress_view(request):
	return render(request, 'dashboard/work-in-progress.html')

""" action functions
They perform some actions - like saving questions to the database
"""
def submit_questions(request):
	question_text_list = request.POST.getlist('question-text')
	question_language_list = request.POST.getlist('question-language')
	question_text_english_list = request.POST.getlist('question-text-english')
	student_name_list = request.POST.getlist('student-name')
	student_class_list = request.POST.getlist('student-class')

	for i in range(len(question_text_list)):
		
		question = Question(
			school = request.POST['school-name'],
			area = request.POST['area'],
			state = request.POST['state'],
			question_format = request.POST['question-format'],
			contributor = request.POST['contributor-name'],
			contributor_role = request.POST['contributor-role'],
			context = request.POST['context'],
			curriculum_followed = request.POST['curriculum-followed'],
			medium_language = request.POST['medium-language'],
			question_text = question_text_list[i],
			question_language = question_language_list[i],
			question_text_english = question_text_english_list[i],
			student_name = student_name_list[i],
			student_class = student_class_list[i] if student_class_list[i] else 0,
			notes = request.POST['notes']
		)

		if (request.POST['published'] == 'Yes'):
			question.published = True
			question.published_source = request.POST['published-source']
			question.published_date = request.POST['published-date']
		else:
			question.published = False

		if (request.POST['question-asked-on']):
			question.question_asked_on = request.POST['question-asked-on']

		question.save()

	context = {
		'number_of_questions_submitted': len(question_text_list),
	}
	
	return render(request, 'dashboard/questions-submitted-successfully.html', context)

def submit_excel_sheet(request):
	
	file = pd.read_excel(request.FILES[request.POST['excel-file-name']])
	columns = list(file)

	column_name_mapping = {
		'Question': 'question_text',
		'Question Language': 'question_language',
		'English translation of question': 'question_text_english',
		'How was the question originally asked?': 'question_format',
		'Context': 'context',
		'When was the question asked?': 'question_asked_on',
		'Student Name': 'student_name',
		'Student Class': 'student_class',
		'School Name': 'school',
		'Curriculum followed' : 'curriculum_followed',
		'Medium of instruction': 'medium_language',
		'Area': 'area',
		'State': 'state',
		'Published': 'published',
		'Publication Name': 'published_source',
		'Publication Date': 'published_date',
		'Notes': 'notes',
		'Contributor Name': 'contributor',
		'Contributor Role': 'contributor_role'
	}

	for index, row in file.iterrows():
		
		question = Question()

		for column in columns:
			if not row[column] != row[column]: # check if the value is not nan

				if column == 'Published':
					setattr(question, column_name_mapping[column], True if row[column] == 'Yes' else False)
				else:	
					setattr(question, column_name_mapping[column], row[column])

		question.save()

	return HttpResponse("Excel sheet saved!")