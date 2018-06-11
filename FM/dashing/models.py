from django.db import models
from django.urls import reverse
import uuid  # Required for unique task instances


# Create your models here.
class Task(models.Model):
    # Fields
    CURRENCY_LIST = (
        ('btcusd', 'American Dollar'),
        ('btcaud', 'Australian Dollar'),
        ('btccad', 'Canadian Dollar'),
        ('btcgbp', 'English Pound'),
        ('btceur', 'Euro'),
        ('btccny', 'Chinese Yuan'),
    )
    currency = models.CharField(max_length=6, choices=CURRENCY_LIST, blank=True, default='btcusd',
                                help_text="Choose a currency you prefer to monitor.")
    TASK_STATUS = (
        ('s', 'Start'),
        ('f', 'Finish'),
        ('p', 'Pending'),
    )
    status = models.CharField(max_length=1, choices=TASK_STATUS, blank=True, default='p', help_text='Task Pending.')
    time_start = models.DateTimeField(null=True, blank=True, help_text='Time the task starts')
    time_finish = models.DateTimeField(null=True, blank=True, help_text='Time the task finishes')

    def __str__(self):
        """
        String presenting this Model
        """
        return "Task: {0}({1})".format(self.currency, self.id)

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('task-detail', args=[str(self.id)])

    class Meta:
        ordering = ['id']


class Query(models.Model):
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular task")
    time_add = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True)
    price_starts = models.FloatField(
        help_text='Enter a starting price.(e.g. 1000. This should smaller than ending price)')
    price_ends = models.FloatField(
        help_text='Enter a ending prince.(e.g. 2000. This should bigger than starting price )')
    target_amount = models.IntegerField(
        help_text='Enter a target amount(integer only, e.g. 500) to monitor')
    QUERY_STATUS = (
        ('a', 'Active'),
        ('m', 'Mature'),
        ('c', 'Completed'),
        ('d', 'Disable'),
    )
    status = models.CharField(max_length=1, choices=QUERY_STATUS, blank=True, default='a', help_text='Task Active')
    time_mature = models.DateTimeField(null=True, blank=True, help_text='Record mature time for this query')

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('query-detail', args=[str(self.id)])

    def __str__(self):
        """
        String presenting this Model
        """
        return "{0} {1}: Range({2}, {3});  Target: {4};  Status: {5}.".format(
            self.task.currency, self.task.id, self.price_starts, self.price_ends, self.target_amount, self.status)

    class Meta:
        ordering = ['task', '-time_add']


class Notification(models.Model):
    message = models.CharField(max_length=6, help_text='Notification message body')
    time_add = models.DateTimeField(auto_now_add=True)
    query = models.ForeignKey('Query', on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('notification-detail', args=[str(self.id)])

    def __str__(self):
        """
        String presenting this Model
        """
        return "Notification: Congratulations! {}".format(self.message)

    class Meta:
        ordering = ['-time_add']