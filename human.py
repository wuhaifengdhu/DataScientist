#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.store_helper import StoreHelper
from lib.text_helper import TextHelper
from lib.csv_helper import CsvHelper
from lib.dict_helper import DictHelper
from lib.segment_helper import SegmentHelper
import pandas as pd


class Main(object):
    @staticmethod
    def generate_profile_summary():
        profile_list = StoreHelper.load_data("./resource/convert_profile.dat", [])
        print (len(profile_list))
        company_dict = StoreHelper.load_data('rank-company_posts_profiles.dic', {})
        rank_dict = StoreHelper.load_data('university_rank.dic')
        top_50_company_employees = []
        for rank, person_detail in company_dict[2]:
            top_50_company_employees.extend(person_detail[1])
        top_50_company_employees = list(set(top_50_company_employees))
        total_company_employees = [i for i in range(len(profile_list))]
        others = list(set(total_company_employees) - set(top_50_company_employees))

        for c_rank, employee_list in {"top 50": top_50_company_employees, "others": others, "total": total_company_employees}.items():
            csv_header = ['employee', 'skills', "work_change_times", "years", "university", "education", "company", "major"]
            csv_data = []
            for employee in employee_list:
                csv_data.append([employee, profile_list[employee]["skills"], profile_list[employee]["work_change_times"], profile_list[employee]["years"], profile_list[employee]["university"], profile_list[employee]["education"], profile_list[employee]["company"],
                                 profile_list[employee]["major"]])
            CsvHelper.write_list_to_csv('%s.csv' % c_rank, csv_header, csv_data)

    # @staticmethod
    # def generate_work_change_times():
    #     csv_header = ['']
    #     csv_header.extend([str(i) for i in range(15)])
    #     csv_header.extend(['>=15'])
    #     csv_data = []
    #     for rank, employee_list in {"1_top 50": top_50_company_employees, "2_others": others,
    #                                 "3_total": total_company_employees}.items():
    #         work_year_dict = {}
    #         for employee in employee_list:
    #             year = profile_list[employee]['work_change_times']
    #             if year == 0:
    #                 print ("zero")
    #             if year < 15 and year < 60:
    #                 DictHelper.increase_dic_key(work_year_dict, str(year))
    #                 print (str(year))
    #             else:
    #                 DictHelper.increase_dic_key(work_year_dict, '>=15')
    #         work_year_list = [rank]
    #         work_year_list.extend([work_year_dict[str(i)] if str(i) in work_year_dict else '0' for i in range(15)])
    #         work_year_list.extend([work_year_dict['>=15']])
    #         csv_data.append(work_year_list)
    #     CsvHelper.write_list_to_csv('working_year_overview.csv', csv_header, csv_data)

    # csv_header = ['', '0']
    # csv_header.extend(['(%d, %d]' % (i, i + 2) for i in range(0, 20, 2)])
    # csv_header.extend(['(40,]'])
    # csv_data = []
    # for rank, employee_list in {"1_top 50": top_50_company_employees, "2_others": others,
    #                             "3_total": total_company_employees}.items():
    #     work_year_dict = {}
    #     for employee in employee_list:
    #         year = profile_list[employee]['years']
    #         if year == 0:
    #             print ("0")
    #             DictHelper.increase_dic_key(work_year_dict, '0')
    #         elif year > 40:
    #             DictHelper.increase_dic_key(work_year_dict, '(40,]')
    #         else:
    #             i = int(year / 2) * 2
    #             DictHelper.increase_dic_key(work_year_dict, '(%d, %d]' % (i, i + 2))
    #     work_year_list = [rank, work_year_dict['0'] if '0' in work_year_dict else '0']
    #     work_year_list.extend(
    #         [work_year_dict['(%d, %d]' % (i, i + 2)] if '(%d, %d]' % (i, i + 2) in work_year_dict else '0' for i in
    #          range(0, 20, 2)])
    #     work_year_list.extend([work_year_dict['(40,]']])
    #     csv_data.append(work_year_list)
    # CsvHelper.write_list_to_csv('working_year_overview.csv', csv_header, csv_data)

    # csv_header = ['', '1-100', '101-200', '201-300', '301-400', '401-500', '501-600', '601-700', '701-800', '801-900',
    #               '901-1000', '1000+']
    # csv_data = []
    # for c_rank, employee_list in {"1_top 50": top_50_company_employees, "2_others": others,
    #                               "3_total": total_company_employees}.items():
    #     university_rank_dict = {}
    #     for employee in employee_list:
    #         university = profile_list[employee]['university']
    #         if university not in rank_dict:
    #             DictHelper.increase_dic_key(university_rank_dict, '1000+')
    #         else:
    #             rank = rank_dict[university]
    #             if rank <= 100:
    #                 DictHelper.increase_dic_key(university_rank_dict, '1-100')
    #             elif rank <= 200:
    #                 DictHelper.increase_dic_key(university_rank_dict, '101-200')
    #             elif rank <= 300:
    #                 DictHelper.increase_dic_key(university_rank_dict, '201-300')
    #             elif rank <= 400:
    #                 DictHelper.increase_dic_key(university_rank_dict, '301-400')
    #             elif rank <= 500:
    #                 DictHelper.increase_dic_key(university_rank_dict, '401-500')
    #             elif rank <= 600:
    #                 DictHelper.increase_dic_key(university_rank_dict, '501-600')
    #             elif rank <= 700:
    #                 DictHelper.increase_dic_key(university_rank_dict, '601-700')
    #             elif rank <= 800:
    #                 DictHelper.increase_dic_key(university_rank_dict, '701-800')
    #             elif rank <= 900:
    #                 DictHelper.increase_dic_key(university_rank_dict, '801-900')
    #             elif rank <= 1000:
    #                 DictHelper.increase_dic_key(university_rank_dict, '901-1000')
    #     new_list = [c_rank]
    #     for i in range(10):
    #         key = "%d-%d" % (i * 100 + 1, (i + 1) * 100)
    #         if key in university_rank_dict:
    #             new_list.append(university_rank_dict[key])
    #         else:
    #             new_list.append('0')
    #     new_list.append(university_rank_dict["1000+"])
    #     csv_data.append(new_list)
    # CsvHelper.write_list_to_csv('university_overview.csv', csv_header, csv_data)

    @staticmethod
    def generate_university_rank(rank_file='./resource/world_university_rank.csv'):
        df = pd.read_csv(rank_file)
        row, column = df.shape
        rank_dict = {}
        university_name_convert_dict = {}
        for i in range(row):
            names = TextHelper.clean_unicode_text(unicode(df['Name'][i], 'ISO-8859-1')).lower().split('|')
            if len(names) == 0:
                continue
            names = [SegmentHelper.normalize_without_lemmatization(name) for name in names]
            full_name = TextHelper.find_max_length_str_in_list(names)
            if len(full_name) > 0:
                rank_dict[full_name] = i
            for name in names:
                if len(name) > 0:
                    university_name_convert_dict[name] = full_name
        StoreHelper.store_data(rank_dict, 'university_rank.dic')
        StoreHelper.store_data(university_name_convert_dict, 'university_name_convert.dic')


if __name__ == '__main__':
    # university_name_convert_dict = StoreHelper.load_data('university_name_convert.dic', {})
    # StoreHelper.save_file(university_name_convert_dict, 'university_name_convert.txt')
    Main.generate_profile_summary()
    # Main.generate_university_rank()