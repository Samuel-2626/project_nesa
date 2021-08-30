from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from ckeditor_uploader.fields import RichTextUploadingField



def validate_image(image):
    file_size = image.file.size
    limit_kb = 50
    if file_size > 0.05*1024*1024:
        raise ValidationError("Max size of image is %s KB" % 50)

class Profile(models.Model):

    STATUS_LEVEL = (

      ('100', '100 level'),
      ('200', '200 level'),
      ('300', '300 level'),
      ('400', '400 level'),
      ('500', '500 level'),
      ('600', '600 level'),
      ('g', 'Graduate'),

    )

    STATUS_UNIVERSITY = (

      ('ABSU', 'Abia State University'),
      ('ATBU', 'Abubakar Tafawa Balewa University'),
      ('AC', 'Achievers University'),
      ('ADSU', 'Adamawa State University'),
      ('AAUA', 'Adekunle Ajasin University'),
      ('ABUAD', 'Afe Babalola University'),
      ('ABU', 'Ahmadu Bello University'),
      ('ACU', 'Ajayi Crowther University'),
      ('AKSU', 'Akwa Ibom State University'),
      ('AHU', 'Al-Hikmah University'),
      ('AAU', 'Ambrose Alli University'),
      ('AUN', 'American University of Nigeria'),
      ('ANSU', 'Anambra State University'),
      ('BU', 'Babcock University'),
      ('BTU', 'Bakassi Technical University'),
      ('BSU', 'Bauchi State University'),
      ('BUK', 'Bayero University'),
      ('BUT', 'Bells University of Technology'),
      ('BIU', 'Benson Idahosa University'),
      ('BSU', 'Benue State University'),
      ('BU', 'Bowen University'),
      ('YSU', 'Bukar Abba Ibrahim University'),
      ('CUl', 'Caleb University'),
      ('CU', 'Caritas University'),
      ('CCU', 'CETEP City University'),
      ('CUY', 'City University'),
      ('CUT', 'City University of Technology'),
      ('CGU', 'Citygate University'),
      ('CNU', 'Covenant University'),
      ('CFU', 'Crawford University'),
      ('CSU', 'Crescent University'),
      ('CRUTECH', 'Cross River University of Technology'),
      ('CHU', 'Crownhill University'),
      ('DELSU', 'Delta State University, Abraka'),
      ('EBSU', 'Ebonyi State University'),
      ('BU', 'ECWA Bingham University'),
      ('EZU', 'Elizade University'),
      ('ESUST', 'Enugu State University of Science and Technology'),
      ('EUA', 'Evangel University, Akaeze'),
      ('FUNAI', 'Federal University Ndufe Alike, Ikwo'),
      ('FUNAAB', 'Federal University of Agriculture, Abeokuta'),
      ('FUTA', 'Federal University of Technology Akure'),
      ('FUBK', 'Federal University, Birnin Kebbi'),
      ('FUG', 'Federal University Gashua'),
      ('FUGU', 'Federal University Gusau'),
      ('FUD', 'Federal University of Dutse'),
      ('FUOYE', 'Federal University Oye-Ekiti'),
      ('FUDM', 'Federal University, Dutsin-Ma'),
      ('FUPRE', 'Federal University of Petroleum Resource Effurun'),
      ('FUTM', 'Federal University of Technology Minna'),
      ('FUTO', 'Federal University of Technology Owerri'),
      ('FUO', 'Fountain University, Osogbo'),
      ('GOU', 'Godfrey Okoye University'),
      ('GSU', 'Gombe State University'),
      ('GSUSTK', 'Gombe State University of Science and Technology, Kumo'),
      ('GU', 'Gregory University'),
      ('IBU', 'Ibrahim Babangida University'),
      ('IUO', 'Igbinedion University'),
      ('IAUE', 'Ignatius Ajuru University of Education'),
      ('IMU', 'Imo State University'),
      ('IOI', 'International Open Institute'),
      ('IMT', 'Institute of Management and Technology,'),
      ('JABU', 'Joseph Ayo Babalola University'),
      ('KSU', 'Kaduna State University'),
      ('KSUST', 'Kano State University of Science and Technology'),
      ('KSUTA', 'Kebbi State University of Technology Aliero'),
      ('KSU', 'Kogi State University'),
      ('KU', 'Koladaisi University'),
      ('KSUY', 'Kwara State University'),
      ('LAUTECH', 'Ladoke Akintola University of Technology'),
      ('LBS', 'Lagos Business School'),
      ('LSU', 'Lagos State University'),
      ('LU', 'Landmark University'),
      ('LCU', 'Lead City University'),
      ('MU', 'Madonna University (Ihiala)'),
      ('MCIU', 'Michael and Cecilia Ibru University'),
      ('MOFUA', 'Michael Okpara Federal University of Agriculture'),
      ('MCIU', 'Michael and Cecilia Ibru University'),
      ('MAUT', 'Modibbo Adama University of Technology'),
      ('MTU', 'Mountain Top University'),
      ('NSU', 'Nasarawa State University'),
      ('NOUN', 'National Open University of Nigeria'),
      ('NDU', 'Niger Delta University'),
      ('NDA', 'Nigerian Defence Academy'),
      ('NTNL', 'Nigerian Turkish Nile University'),
      ('NAU', 'Nnamdi Azikiwe University'),
      ('NWU', 'Northwest University'),
      ('NU', 'Novena University'),
      ('OAU', 'Obafemi Awolowo University'),
      ('OU', 'Obong University,'),
      ('OUI', 'Oduduwa University'),
      ('OOU', 'Olabisi Onabanjo University'),
      ('OSUSST', 'Ondo State University of Science and Technology'),
      ('UNIOSUN', 'Osun State University'),
      ('PAU', 'Pan-Atlantic University'),
      ('PU', 'Paul University'),
      ('PSUB', 'Plateau State University Bokkos'),
      ('RUN', 'Redeemer\'s University Nigeria'),
      ('RU', 'Renaissance University'),
      ('RU', 'Rhema University'),
      ('RTU', 'Ritman University'),
      ('RSU', 'Rivers State University'),
      ('SU', 'Salem University'),
      ('SAU', 'Samuel Adegboyega University'),
      ('SUN', 'Skyline University Nigeria'),
      ('SSU', 'Sokoto State University'),
      ('SLU', 'Sule Lamido University'),
      ('TSUE', 'Tai Solarin University of Education'),
      ('TSU', 'Taraba State University'),
      ('TUI', 'The University on Idemili'),
      ('UMYUK', 'Umaru Musa Yar\'adua University Katsina'),
      ('UA', 'University of Abuja'),
      ('UAE', 'University of Ado Ekiti'),
      ('UAA', 'University of Agriculture, Abeokuta'),
      ('UATO', 'University of Africa(Toru-Orua)'),
      ('UAM', 'University of Agriculture, Makurdi'),
      ('UC', 'University of Calabar'),
      ('UO', 'University of Ibadan'),
      ('UNIILORIN', 'University of Ilorin'),
      ('UJ', 'University of Jos'),
      ('UNILAG', 'University of Lagos'),
      ('UM', 'University of Maiduguri'),
      ('UMK', 'University of Mkar'),
      ('UNN', 'University of Nigeria, Nsukka'),
      ('UPH', 'University of Port Harcourt'),
      ('UU', 'University of Uyo'),
      ('UDFU', 'Usman Dan Fodio University'),
      ('WU', 'Wesley University'),
      ('WDU', 'Western Delta University'),
      ('VU', 'Veritas University'),
      ('YCT', 'Yaba College of Technology, Yaba'),
      

    )

    STATUS_FACULTY = (
      ('FAS', 'Faculty of Agricultural Sciences'),
      ('FAT', 'Faculty of Arts'),
      ('DEGS', 'Directorate for Entrepreneurship And General Studies (DE&GS)'),
      ('FE', 'Faculty of Education'),
      ('FHS', 'Faculty of Health Sciences'),
      ('FL', 'Faculty of Law'),
      ('FMS', 'Faculty of Management Sciences'),
      ('FS', 'Faculty of Science'),
      ('FSS', 'Faculty of Social Sciences'),
    )

    STATUS_DEPARTMENT = (
      ('ACC', 'Accountancy'),
      ('AS', 'Acturial Science'),
      ('ADEES', 'Adult Education and Extra-Mural Studies'),
      ('AG', 'Agriculture'),
      ('AE', 'Agricultural Economics'),
      ('AXD', 'Agricultural Extension'),
      ('A', 'Agronomy'),
      ('ASC', 'Animal Science'),
      ('AIS', 'Arabic and Islamic Studies'),
      ('AT', 'Archeology and Tourism'),
      ('AE', 'Arts Education'),
      ('BFN', 'Banking and Finance'),
      ('BCH', 'Biochemistry'),
      ('BY', 'Botany'),
      ('BUA', 'Business Administration'),
      ('BM', 'Business Management'),
      ('CBG', 'Cell Biology & Genetics'),
      ('CDH', 'Child Dental Health'),
      ('CRS', 'Christian Religious Studies'),
      ('CS', 'Crop Science'),
      ('ECN', 'Economics'),
      ('EA', 'Education & Accountancy'),
      ('EB', 'Education & Biology'),
      ('EC', 'Education & Chemistry'),
      ('ECS', 'Education & Computer Science'),
      ('EE', 'Education & Economics'),
      ('EEL', 'Education & English Language'),
      ('EF', 'Education & French'),
      ('EM', 'Education & Mathematics'),
      ('EP', 'Education & Physics'),
      ('EPS', 'Education & Political Science'),
      ('ERS', 'Education & Religious Studies'),
      ('ESS', 'Education & Social Science'),
      ('EF', 'Educational Foundations'),
      ('EPGC', 'Educational / Psychology Guidance And Counselling'),
      ('ELS', 'English and Literary Studies'),
      ('FST', 'Food Science and Technology'),
      ('FAA', 'Fine and Applied Arts (Creatiuve Arts)'),
      ('F', 'Fisheries'),
      ('FLL', 'Foreign Languages and Literature'),
      ('FRM', 'Forest Resources Management (Forestry)'),
      ('GEO', 'Geography'),
      ('HPE', 'Health and Physical Education'),
      ('HIS', 'History and International Studies'),
      ('HSND', 'Home Science, Nutrition and Dietetics'),
      ('HT', 'Hospitality and Tourism'),
      ('HRM', 'Human Resource Management'),
      ('IL', 'Igbo Linguistics'),
      ('IRPM', 'Industrial Relations and Personnel Management'),
      ('I', 'Insurance'),
      ('LIS', 'Library and Information Science'),
      ('LNL', 'Linguistics and Nigerian Languages'),
      ('M', 'Marketing'),
      ('MB', 'Marine Biology'),
      ('MC', 'Mass Communication (Communication and Language Arts)'),
      ('MCB', 'Microbiology'),
      ('MU', 'Music'),
      ('OMS', 'Oral and Maxillofacial Surgery'),
      ('POL', 'Political Sciences'),
      ('PD', 'Preventive Dentistry'),
      ('PHIL', 'Philosophy'),
      ('PSY', 'Psychology'),
      ('RS', 'Religious Studies'),
      ('RD', 'Restorative Dentistry'),
      ('SE', 'Science Education'),
      ('SSE', 'Social Sciences Education'),
      ('SOC', 'Sociology'),
      ('SS', 'Soil Science'),
      ('TFS', 'Theatre and Film Studies'),
      ('VTE', 'Vocational Teacher Education (Technical Education)'),
      ('Z', 'Zoology'),
      
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = RichTextUploadingField(help_text='Provide Short description of yourself',  max_length=200, blank=True, null=True)
    university = models.CharField(max_length=10, choices=STATUS_UNIVERSITY, null=True, blank=True)
    faculty = models.CharField(max_length=10, choices=STATUS_FACULTY, null=True, blank=True)
    department = models.CharField(max_length=10, choices=STATUS_DEPARTMENT, null=True, blank=True)
    level = models.CharField(max_length=10, choices=STATUS_LEVEL, null=True, blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, validators=[validate_image],)

    facebook_name = models.CharField(help_text='e.g Please provide a valid username',  max_length=500, blank=True, null=True)
    instagram_name = models.CharField(help_text='e.g Please provide a valid username',  max_length=500, blank=True, null=True)
    twitter_name = models.CharField(help_text='e.g Please provide a valid username',  max_length=500, blank=True, null=True)
    linkedin_name = models.CharField(help_text='e.g Please provide a valid username',  max_length=500, blank=True, null=True)
    website = models.CharField(help_text='e.g Please provide a link to your website',  max_length=500, blank=True, null=True)
    
    reputation = models.PositiveBigIntegerField(default=0, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    
    
    
    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "/static/images/no-image.png"
    
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    


class ProfileViews(models.Model):

  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_views')
  host = models.CharField(max_length=500)
  ip = models.GenericIPAddressField()
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('-created',)
    unique_together = ['profile', 'ip']

  def __str__(self):
      return self.ip