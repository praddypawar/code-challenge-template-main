from django.core.management.base import BaseCommand

from app.models import Weather,DataAnalysis
from django.db.models import Max, Min, Avg, Sum
import datetime
from django.db.models.functions import TruncMonth, TruncYear


class Command(BaseCommand):
    help = 'Analyze aand insert/update Weather Statistics Data'

    def add_argument(self, parser):
        pass

    def format_date(self, date):
        return f'{date[:4]}-{date[4:6]}-{date[6:]}'

    def handle(self, *args, **options):
        # num_of_records_before_insert = DataAnalysis.objects.all().count()
        # start_time = datetime.datetime.now()
        # weather_data = Weather.objects.all().count()
        # if weather_data == 0:
        #     print("No Data available to analyze weather")

        # start_year = Weather.objects.aggregate(Min("date"))['date__min'].year
        # end_year = Weather.objects.aggregate(Max("date"))['date__max'].year

        # all_stations = set(Weather.objects.values_list("station_id"))
        # for station in all_stations:
        #     temp_start_year = start_year
        #     while temp_start_year <= end_year:

        #         avg_max_temp = Weather.objects.exclude(max_temp=-9999).filter(station_id=station[0],date__year=temp_start_year).aggregate(Avg("max_temp"))['max_temp__avg']

        #         avg_min_temp = Weather.objects.exclude(max_temp=-9999).filter(station_id=station[0],date__year=temp_start_year).aggregate(Avg("min_temp"))['min_temp__avg']
        #         total_precipitation = Weather.objects.exclude(precipitation=-9999).filter(station_id=station[0],date__year=temp_start_year).aggregate(Sum("precipitation"))['precipitation__sum']

        #         # Updating or inserting weather statistics data into Statistics table
        #         DataAnalysis.objects.update_or_create(station_id=station[0], year=temp_start_year,
        #                                             max_temp_avg=avg_max_temp, min_temp_avg=avg_min_temp,
        #                                             total_precipitation=total_precipitation)
        #         # print(f'Weather statistics for Station_id-{station[0]}: year{temp_start_year} are inserted into the database')
        #         temp_start_year += 1

        # finish_time = datetime.datetime.now()
        # num_of_records_after_insert = DataAnalysis.objects.all().count()


        num_of_records_before_insert = DataAnalysis.objects.all().count()
        start_time = datetime.datetime.now()
        weather_data = Weather.objects.all().count()
        if weather_data == 0:
            print("No Data available to analyze weather")

        w_data = list(Weather.objects.exclude(max_temp=-9999,precipitation=-9999).annotate(year=TruncYear('date')).values("station_id","date__year").annotate(max_temp_avg=Avg('max_temp'),min_temp_avg=Avg('min_temp'),total_precipitation=Sum('precipitation')))
        
        products = []
        
        
        print(len(w_data))
        for i in range(len(w_data)):
            products.append(
                DataAnalysis(
                station_id=w_data[i]["station_id"],
                year = w_data[i]["date__year"],
                max_temp_avg = w_data[i]["max_temp_avg"],
                min_temp_avg = w_data[i]["min_temp_avg"],
                total_precipitation = w_data[i]["total_precipitation"],
                )
            )
        DataAnalysis.objects.bulk_create(products,ignore_conflicts=True)

        finish_time = datetime.datetime.now()
        num_of_records_after_insert = DataAnalysis.objects.all().count()

        # using print as log statement for test purposes
        print("Weather statistics data \n")
        print(f"Start Time {start_time}" + "\n")
        print(f"Finish Time {finish_time}" + "\n")
        print(f"Number of records ingested: {num_of_records_after_insert - num_of_records_before_insert}" + "\n")
        print(f"Execution time =  {finish_time - start_time} \n")
        

