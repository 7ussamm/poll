from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1) # attach the user to the poll
    text = models.CharField(max_length=255)
    number = models.CharField(max_length=255)

    # to make the text appears on the admin panel
    def __str__(self):
        return self.text # this text is the previous variable


    def user_can_vote(self, user):
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property # to be able to call it directly anywhere
    def num_votes(self):
        return self.vote_set.count()

    def get_percentages(self):
        resault = []
        for choice in self.choices_set.all(): # self refering to Poll class
            dict = {}
            dict['text'] = choice.choice_text
            dict['num_choice'] = choice.num_choices
            if not self.num_votes:
                dict['percentage'] = 0
            else:
                dict['percentage'] = choice.num_choices / self.num_votes * 100
            resault.append(dict)
        return resault


class Choices(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE) # connecting with the previous class
    choice_text = models.CharField(max_length=250) # adding the votes choices into it
    # vote = models.IntegerField(default=0)   # counting how many times the votes happened

    def __str__(self):
        return ' {} - {} '.format(self.poll.text, self.choice_text)
        '''
            previous return statement makes it appear on the shell like this:

            <QuerySet [<Choices:  Te gusta Django ? - Si - 0>, <Choices:  Te gusta Django ? - Si, Claro - 0>]>

            using:
            var = Poll.objects.first() # gets the first object from polls with it's answers
            var.choices_set.all()      # that's what will cause the previous display
                                       # able to use var.choices_set just like var.objects

            explain:
            [<Choices:
                        Te gusta Django ? # self.question.text
                        - Si              # self.choice_text
                        - 0               # self.vote
            >]

            Able to add another choices directly from the Shell using create keyword:
                var.choices_set.create(choice_text='No, Nunca') # NOTICE choice_text


            ## NOTICE that u have to import Choices and Poll before excuting previous commands

            ## ALSO NOTICE THAT the resault of the two commands
                Choices.objects.all()
                var.choices_set.all()
               THEY are the same resaults, that's cuz of the ForeignKey statement earlier
               which connected the two classes together
        '''

    @property # to be able to call it directly anywhere
    def num_choices(self):
            return self.vote_set.count()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choices, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice.choice_text
