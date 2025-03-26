from django.db import models

# Create your models here.

class User(models.Model):
    Forename = models.CharField(max_length=255)
    Surname = models.CharField(max_length=255)
    DOB = models.DateField()
    #could also have username be unique
    Email = models.CharField(max_length=255, unique=True)
    Contact = models.CharField(max_length=255)
    #why is telephone maxlength 20?
    Telephone = models.CharField(max_length=20)
    Username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)


    def __str__(self):
        return self.Forename +" "+ self.Surname
    

class Membership(models.Model):
    MembershipType = [
        ("MONTHLY", "Monthly"),
        ("QUARTERLY", "Quarterly"),
        ("ANNUAL", "Annual"),
    ]

    #ID = models.CharField(max_length=25, unique=True)
    Start = models.DateField()
    End = models.DateField()
    Type = models.CharField(max_length=9, choices=MembershipType)

    #def __str__(self):
     #   return self.ID
    

class Booking(models.Model):
    RefNo = models.CharField(max_length=25)

    def __str__(self):
        return self.RefNo
        


class Activity(models.Model):
    Title = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    Start = models.DateField()
    End = models.DateTimeField()
    Date = models.DateField()
    Capacity = models.SmallIntegerField()  


    def __str__(self):
        return self.Title + "\n" + self.Description
        

class Payment(models.Model):
    TransactionNo = models.CharField(max_length=25, unique=True)
    # may need adjustment to be 2.99 rather than something like 2.9975? decimal places n all that
    Amount = models.DecimalField        

    def __str__(self):
        return self.TransactionNo
    



class Facility(models.Model):
    RoomStatus = [
        ("FREE", "Free"),
        ("RESERVED", "Reserved"),
    ]

    RoomName = models.CharField(max_length=25, unique=True)
    Description = models.CharField(max_length=255)
    #what kind of enum is this supposed to be? I've assumed 'free' and 'reserved' 
    # but this doesn't really allow for planning multiple activities. correct if you want. 

    Status = models.CharField(max_length=8, choices=RoomStatus)

    def __str__(self):
        return self.RoomName    



class Staff(models.Model):
    StaffID = models.CharField(max_length=25, unique=True)
    JobTitle = models.CharField(max_length=25)

    def __str__(self):
        return self.StaffID
    

class Announcement(models.Model):
    DateTime = models.DateTimeField()
    Content = models.CharField(max_length=255)             
    
    def __str__(self):
        return self.Content
    

class Feedback(models.Model):
    RefNo = models.CharField(max_length=25, unique=True)
    Content = models.CharField(max_length=255)   
    
    def __str__(self):
        return self.RefNo
        
    
    