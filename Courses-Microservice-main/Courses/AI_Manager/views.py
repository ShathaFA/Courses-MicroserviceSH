from rest_framework import generics, status
from rest_framework.response import Response
from courseAdminstration.models import Course, Section, Lesson, Content
from .serializers import GenerateCourseContentSerializer, GenerateLessonContentSerializer
import re
import openai
from rest_framework.exceptions import APIException
import concurrent.futures

# Set your OpenAI API key
openai.api_key = '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'
class GenerateCourseContentAPIView(generics.CreateAPIView):
    serializer_class = GenerateCourseContentSerializer

    def create(self, request, *args, **kwargs):
        try:
            if not openai.api_key:
                raise APIException("OpenAI API key is not set")

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            title = serializer.validated_data.get('title')
            category = serializer.validated_data.get('category')
            difficultyLevel = serializer.validated_data.get('difficultyLevel')
            number_of_sections = serializer.validated_data.get('number_of_sections')

            # Placeholder value for instructor ID
            instructor_id = 8  # Replace '1' with the actual instructor ID or logic to fetch the instructor ID

            # Create course with instructor ID provided
            course = Course.objects.create(title=title, difficultyLevel=difficultyLevel, category=category, instructor=instructor_id)

            # Generate course description
            course_description = self.generate_course_description(title, category, difficultyLevel)
            course.description = course_description
            course.save()

            prompt = f"I want you to generate a complete course using this information: {{ title: {title}, Category: {category}, Level: {difficultyLevel} }} Please provide the following first: number_of_sections, then the structure of the course generated should follow the number of course sections, then the title of the section generated, then under it the lesson name and number."

            # Generate course content asynchronously
            content = self.generate_course_content(prompt)

            if not content:
                raise APIException("Failed to generate course content")

            sections = []
            section_pattern = r"Section (\d+): (.*?)\n((?:Lesson \d+: (.*?)\n)+)"
            matches = re.findall(section_pattern, content)[:number_of_sections]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Generate lesson contents in parallel
                lesson_contents = list(executor.map(self.generate_lesson_content, [lesson_match[1] for match in matches for lesson_match in re.findall(r"Lesson (\d+): (.*?)\n", match[2])]))

                for match, lesson_content in zip(matches, lesson_contents):
                    section_number = int(match[0])
                    section_title = match[1]

                    # Create section object
                    section = Section.objects.create(title=section_title, course=course)

                    # Generate section description
                    section_description = self.generate_section_description(section_title)
                    section.description = section_description
                    section.save()

                    lessons = []
                    lesson_matches = re.findall(r"Lesson (\d+): (.*?)\n", match[2])
                    for lesson_match, lesson_content in zip(lesson_matches, lesson_contents):
                        lesson_number = int(lesson_match[0])
                        lesson_title = lesson_match[1]

                        # Create lesson and content objects
                        lesson = Lesson.objects.create(title=lesson_title, section=section)
                        Content.objects.create(lesson=lesson, type='txt', text_content=lesson_content.strip())  # Changed from 'reference' to 'text_content'
                        # Append lesson details to lessons list
                        lessons.append({
                            'number': lesson_number,
                            'title': lesson_title,
                            'content': lesson_content.strip()
                        })

                    # Append section details to sections list
                    sections.append({
                        'number': section_number,
                        'title': section_title,
                        'description': section_description,  # Include section description in response
                        'lessons': lessons
                    })

            response_data = {
                'message': 'Course content generated successfully',
                'number_of_sections': len(sections),
                'sections': sections
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def generate_course_content(self, prompt):
        client = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=1500  # Adjust the max_tokens value as needed
        )
        return client.choices[0].text.strip() if client.choices else ""

    def generate_course_description(self, title, category, difficulty_level):
        # Generate course description using OpenAI API
        prompt = f"Generate a course description for the course titled: {title}, in the category: {category}, and difficulty level: {difficulty_level}"
        client = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=500  # Adjust the max_tokens value as needed
        )
        return client.choices[0].text.strip() if client.choices else ""

    def generate_section_description(self, section_title):
        # Generate section description using OpenAI API
        prompt = f"Generate a description for the section titled: {section_title}"
        client = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=500  # Adjust the max_tokens value as needed
        )
        return client.choices[0].text.strip() if client.choices else ""

    def generate_lesson_content(self, lesson_title):
        prompt = f"Generate content for the lesson titled: {lesson_title} that is more than 200 words and relevant and useful"
        
        client = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=1000  # Adjust the max_tokens value as needed
        )

        return client.choices[0].text.strip() if client.choices else ""



from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import GenerateMCQsSerializer, QuestionSerializer, QuizSerializer
from courseAdminstration.models import Quiz, Question, Lesson
import openai

# Move API key to a secure location (e.g., environment variable)
openai.api_key = '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'
class GenerateMCQsAPIView(generics.CreateAPIView):
    serializer_class = GenerateMCQsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        topic = serializer.validated_data.get('topic')
        number_of_questions = serializer.validated_data.get('number_of_questions')

        prompt = f"Generate {number_of_questions} multiple choice questions related to the topic: {topic}. No repeated or repeated but paraphrased questions in the response, and each question should have only one correct choice within the generated choices."

        try:
            # Generate MCQs using OpenAI's completion API
            client = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=2500,
                n=int(number_of_questions),
                stop=None
            )
        except openai.error.OpenAIError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lesson_id = serializer.validated_data.get('lesson_id')
        quiz = Quiz.objects.create(mark=0, lesson_id=lesson_id)  # Use lesson_id directly

        questions_data = []
        for index, choice in enumerate(client.choices, start=1):
            question_lines = choice['text'].strip().split('\n')
            question_title = question_lines[0]
            options = [line.strip() for line in question_lines[1:5]]

            correct_choice = None
            for line in question_lines[1:]:
                if line.startswith("Answer:"):
                    correct_choice = line.replace("Answer:", "").strip()
                    break

            if correct_choice not in options:
                # If correct choice is not among the provided options, continue to generate another question
                continue

            formatted_question = {
                "title": question_title,
                "correct_answer": correct_choice,
                "choice1": options[0],
                "choice2": options[1] if len(options) > 1 else "",
                "choice3": options[2] if len(options) > 2 else "",
                "choice4": options[3] if len(options) > 3 else "",
                "quiz": quiz.id
            }
            questions_data.append(formatted_question)

        # Generate additional questions until reaching the desired number
        while len(questions_data) < number_of_questions:
            try:
                client = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=prompt,
                    max_tokens=2500,
                    n=1,  # Generate one additional question
                    stop=None
                )
            except openai.error.OpenAIError as e:
                continue  # Skip this iteration if there's an error

            choice = client.choices[0]
            question_lines = choice['text'].strip().split('\n')
            question_title = question_lines[0]
            options = [line.strip() for line in question_lines[1:5]]

            correct_choice = None
            for line in question_lines[1:]:
                if line.startswith("Answer:"):
                    correct_choice = line.replace("Answer:", "").strip()
                    break

            if correct_choice not in options:
                # If correct choice is not among the provided options, continue to generate another question
                continue

            formatted_question = {
                "title": question_title,
                "correct_answer": correct_choice,
                "choice1": options[0],
                "choice2": options[1] if len(options) > 1 else "",
                "choice3": options[2] if len(options) > 2 else "",
                "choice4": options[3] if len(options) > 3 else "",
                "quiz": quiz.id
            }
            questions_data.append(formatted_question)

        questions_serializer = QuestionSerializer(data=questions_data, many=True)
        questions_serializer.is_valid(raise_exception=True)
        questions_serializer.save()

        quiz.mark = len(questions_data)  # Update quiz mark based on the number of questions generated
        quiz.save()

        quiz_serializer = QuizSerializer(quiz)
        response_data = {
            "quiz": quiz_serializer.data,
            "questions": questions_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
 
from rest_framework import generics, status
from rest_framework.response import Response
from courseAdminstration.models import Course, Section, Lesson, Content
from .serializers import GenerateLessonContentSerializer
import openai
from rest_framework.exceptions import APIException

# Set your OpenAI API key
openai.api_key = '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'

class GenerateLessonContentAPIView(generics.CreateAPIView):
    serializer_class = GenerateLessonContentSerializer

    def create(self, request, *args, **kwargs):
        try:
            if not openai.api_key:
                raise APIException("OpenAI API key is not set")

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            course_name = serializer.validated_data.get('course_name')
            course_description = serializer.validated_data.get('course_description')
            section_name = serializer.validated_data.get('section_name')
            section_description = serializer.validated_data.get('section_description')
            lesson_name = serializer.validated_data.get('lesson_name')

            # Placeholder value for instructor ID
            instructor_id = 8  # Replace '8' with the actual instructor ID or logic to fetch the instructor ID

            # Create course with instructor ID provided
            course = Course.objects.create(title=course_name, description=course_description, instructor=instructor_id)

            # Create section under the course
            section = Section.objects.create(title=section_name, description=section_description, course=course)

            # Generate lesson content based on user input
            lesson_content = self.generate_lesson_content(course_name, course_description, section_name, section_description, lesson_name)

            # Create lesson and content objects
            lesson = Lesson.objects.create(title=lesson_name, section=section)
            Content.objects.create(lesson=lesson, type='txt', text_content=lesson_content.strip())  # Changed from 'reference' to 'text_content'

            response_data = {
                'message': 'Lesson content generated and saved successfully',
                'course_name': course_name,
                'section_name': section_name,
                'lesson_name': lesson_name,
                'lesson_content': lesson_content  # Include the generated lesson content in the response
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def generate_lesson_content(self, course_name, course_description, section_name, section_description, lesson_name):
        prompt = f"Generate content for the lesson '{lesson_name}' using the entered section name '{section_name}' and description '{section_description}' of the course '{course_name}' which has a description '{course_description}' and make the content more than 200 words and relevant and useful"
        
        client = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=1500  # Adjust the max_tokens value as needed
        )

        return client.choices[0].text.strip() if client.choices else ""
