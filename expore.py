#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.store_helper import StoreHelper
from lib.distance_helper import DistanceHelper
from lib.csv_helper import CsvHelper
from lib.text_helper import TextHelper
from lib.dict_helper import DictHelper
import random


class Main(object):
    @staticmethod
    def cross():
        profile_list = StoreHelper.load_data('./resource/convert_profile.dat', [])
        position_dict = StoreHelper.load_data("./data/position_vector_01.dat", {})
        print (len(position_dict.values()[0]))
        vector_list = StoreHelper.load_data('vector.dat', [])
        print (sum([len(value) for value in vector_list]))
        vector_dict = {'years': vector_list[0], 'education': vector_list[1], 'major': vector_list[2],
                       'skills': vector_list[3], 'responsibility': vector_list[4]}
        vector_length = [len(item_list) for item_list in vector_list]
        vector_length_dict = {'years': (0, sum(vector_length[:1])),
                              'education': (sum(vector_length[:1]), sum(vector_length[:2])),
                              'major': (sum(vector_length[:2]), sum(vector_length[:3])),
                              'skills': (sum(vector_length[:3]), sum(vector_length[:4])),
                              'responsibility': (sum(vector_length[:4]), sum(vector_length[:5]))}
        position_list = []
        index_dict = {}
        count = 0
        for index, position in position_dict.items():
            index_dict[count] = index
            count += 1
            position_phrase_dict = {}
            for feature in vector_dict:
                start, end = vector_length_dict[feature]
                for i in range(len(vector_dict[feature])):
                    if position[start + i] > 0:
                        DictHelper.append_dic_key(position_phrase_dict, feature, vector_dict[feature][i])
            position_list.append(position_phrase_dict)
        StoreHelper.store_data(index_dict, 'index_dict.dat')
        StoreHelper.store_data(position_list, 'position_list.dat')
        profile_sum = []
        position_sum = []
        phrase_list = []
        for feature in ['years', 'education', 'major', 'skills']:
            phrase_l, profile_s, position_s = Main.generate_feature_vector(feature, profile_list, position_list)
            phrase_list.extend(phrase_l)
            profile_sum.extend(profile_s)
            position_sum.extend(position_s)
        max_distance = DistanceHelper.compute_distance([i * 1.0 / len(profile_list) for i in profile_sum],
                                                       [i * 1.0 / len(position_list) for i in position_sum])
        csv_column = ["type", "total number"]
        csv_column.extend(phrase_list)
        csv_data = [["profile", len(profile_list)], ["position", len(position_list)]]
        csv_data[0].extend([str(i) for i in profile_sum])
        csv_data[1].extend([str(i) for i in position_sum])
        CsvHelper.write_list_to_csv("sum_total.csv", csv_column, csv_data, sort_data_row=0, escape_first=2,
                                    append_rows=[['cross distance', max_distance]])

    @staticmethod
    def generate_profile_position_common():
        print ("step 1, generate common feature")
        common_feature_dict = {}
        for feature in ['years', 'education', 'major', 'skills']:
            common_feature_dict[feature] = StoreHelper.load_data("position_profile_%s.dat" % feature, [])
            print ("%s: %s" % (feature, common_feature_dict[feature]))
            print ("Load %d phrase for %s" % (len(common_feature_dict[feature]), feature))

        print ("step 2, generate vector for post and profile")
        profile_list = StoreHelper.load_data('./resource/convert_profile.dat', [])
        print ("sample: %s" % profile_list[0])
        total_profile = len(profile_list)
        print ("Load %d profile from file" % total_profile)
        position_list = StoreHelper.load_data('position_list.dat', [])
        print ("sample: %s" % position_list[0])
        total_position = len(position_list)
        print ("Load %d position from file" % total_position)

        skills_convert_dict = StoreHelper.load_data('skills_convert_dict.dat', {})
        print ("Load %d skill convert dict from file" % len(skills_convert_dict))

        profile_vector = []
        position_vector = []
        count = 0
        for profile in profile_list:
            print ("Work on profile %d totally %d" % (count, total_profile))
            count += 1
            profile_dict = {feature: [] for feature in common_feature_dict.keys()}
            for feature in common_feature_dict:
                if feature in profile:
                    for phrase in common_feature_dict[feature]:
                        profile_dict[feature].append(1 if phrase in profile[feature] else 0)
                else:
                    profile_dict[feature] = [0 for i in range(len(common_feature_dict[feature]))]
            profile_vector.append(profile_dict)

        count = 0
        for position in position_list:
            print ("Work on position %d totally %d" % (count, total_position))
            count += 1
            position_dict = {feature: [] for feature in common_feature_dict.keys()}
            for feature in common_feature_dict:
                if feature in position:
                    for phrase in common_feature_dict[feature]:
                        position_dict[feature].append(1 if phrase in position[feature] else 0)
                else:
                    position_dict[feature] = [0 for i in range(len(common_feature_dict[feature]))]
            position_vector.append(position_dict)

        print ("step 3, store into data file")
        print ("Profile sample: %s" % str(profile_vector[0]))
        print ("Position sample: %s" % str(position_vector[0]))
        StoreHelper.store_data(profile_vector, 'profile_vector_common.dat')
        StoreHelper.store_data(position_vector, 'position_vector_common.dat')

    @staticmethod
    def find_position_candidate(position_index, threshold, feature_list=None, min_skill_ratio=None):
        if feature_list is None:
            feature_list = ['years', 'education', 'major', 'skills']
        profile_vector = StoreHelper.load_data('profile_vector_common.dat', [])
        position_vector = StoreHelper.load_data('position_vector_common.dat', [])
        index_dict = StoreHelper.load_data('index_dict.dat', {})

        meet_dict = {}
        if position_index is None:
            count = 0
            total_account = len(position_vector)
            for position in position_vector:
                print ("total position %d now is %d" % (total_account, count))

                distance_list = [Main.generate_match_ratio(position, profile, feature_list, min_skill_ratio)
                                 for profile in profile_vector]
                meet_dict[index_dict[count]] = sum([1 if distance >= threshold else 0 for distance in distance_list])
                count += 1
        else:
            position = position_vector[index_dict[position_index]]
            print ("Position: %s" % str(position))
            distance_list = [Main.generate_match_ratio(position, profile, feature_list, min_skill_ratio)
                             for profile in profile_vector]
            print (distance_list)
            print ("max distance %f" % max(distance_list))
            meet_dict[position_index] = sum([1 if distance >= threshold else 0 for distance in distance_list])
            print ("Totally %d profile meet requirements" % meet_dict[position_index])
        return meet_dict

    @staticmethod
    def find_profile_candidate(profile_index, threshold, feature_list=None, min_skill_ratio=None):
        if feature_list is None:
            feature_list = ['years', 'education', 'major', 'skills']
        profile_vector = StoreHelper.load_data('profile_vector_common.dat', [])
        position_vector = StoreHelper.load_data('position_vector_common.dat', [])

        meet_dict = {}
        if profile_index is None:
            count = 0
            total_account = len(profile_vector)
            for profile in profile_vector:
                print ("total position %d now is %d" % (total_account, count))
                distance_list = [Main.generate_match_ratio(position, profile, feature_list, min_skill_ratio)
                                 for position in position_vector]
                meet_dict[count] = sum([1 if distance >= threshold else 0 for distance in distance_list])
                count += 1
        else:
            profile = profile_vector[profile_index]
            print ("Position: %s" % str(profile))
            distance_list = [Main.generate_match_ratio(position, profile, feature_list, min_skill_ratio)
                             for position in position_vector]
            print (distance_list)
            print ("max distance %f" % max(distance_list))
            meet_dict[profile_index] = sum([1 if distance >= threshold else 0 for distance in distance_list])
            print ("Totally %d profile meet requirements" % meet_dict[profile_index])
        return meet_dict

    @staticmethod
    def generate_cosine_similarity(position, profile, feature_weight_dict):
        position_vector = []
        profile_vector = []
        for feature in feature_weight_dict:
            position_vector.extend(position[feature])
            profile_vector.extend(profile[feature])
        return DistanceHelper.compute_distance(position_vector, profile_vector)

    @staticmethod
    def vector_less_than(vector_a, vector_b):
        if len(vector_b) != len(vector_a):
            print ("Error! year match vector length not equal! %s vs %s" % (str(vector_a), str(vector_b)))
            return 0
        sum_a = 0
        sum_b = 0
        length = len(vector_a)
        for i in range(length - 1, -1, -1):
            sum_a = (sum_a + vector_a[i]) * length
            sum_b = (sum_b + vector_b[i]) * length
        return sum_a <= sum_b

    @staticmethod
    def years_match(vector_position, vector_profile):
        return 1 if Main.vector_less_than(vector_position, vector_profile) else 0

    @staticmethod
    def major_match(vector_position, vector_profile):
        for major in vector_profile:
            if major in vector_position:
                return 1
        return 0

    @staticmethod
    def education_match(vector_position, vector_profile):
        return 1 if Main.vector_less_than(vector_position, vector_profile) else 0

    @staticmethod
    def skills_match(vector_position, vector_profile, match_rate_require=0):
        if len(vector_position) != len(vector_profile):
            print ("Error! year match vector length not equal! %s vs %s" % (str(vector_position), str(vector_profile)))
            return 0
        if sum(vector_position) == 0:
            print ("position with no requirement!")
            return 0
        match_rate = sum([vector_position[i] * vector_profile[i] for i in range(len(vector_position))]) / \
                     (sum(vector_position) * 1.0)
        return 1 if match_rate >= match_rate_require else 0

    @staticmethod
    def skills_match_simple(vector_position, vector_profile):
        if len(vector_position) != len(vector_profile):
            print ("Error! year match vector length not equal! %s vs %s" % (str(vector_position), str(vector_profile)))
            return 0
        if sum(vector_position) == 0:
            print ("position with no requirement!")
            return 1
        match_rate = sum([vector_position[i] * vector_profile[i] for i in range(len(vector_position))]) / \
                     (sum(vector_position) * 1.0)
        return match_rate

    @staticmethod
    def generate_match_ratio(position, profile, feature_list, min_skill_ratio):
        match_dict = {
            'years': Main.years_match, 'education': Main.education_match, 'major': Main.major_match,
            'skills': Main.skills_match
        }
        match_ratio = 1
        for feature in feature_list:
            match_ratio *= match_dict[feature](position[feature], profile[feature])
        if min_skill_ratio is not None:
            match_ratio *= Main.skills_match(position["skills"], profile["skills"], min_skill_ratio)
        return match_ratio

    @staticmethod
    def generate_match_ratio_simple(position, profile, feature_list):
        match_dict = {
            'years': Main.years_match, 'education': Main.education_match, 'major': Main.major_match,
            'skills': Main.skills_match_simple
        }
        match_ratio = 1
        for feature in feature_list:
            match_ratio *= match_dict[feature](position[feature], profile[feature])
        return match_ratio

    @staticmethod
    def test_average_skills_per_post():
        position_list = StoreHelper.load_data('position_list.dat', [])
        skill_number_list = [len(post['skills']) if 'skills' in post else 0 for post in position_list]
        print (skill_number_list)
        print ("total position number %d, average %f skills per post!" % (
        len(position_list), sum(skill_number_list) * 1.0 / len(position_list)))

    @staticmethod
    def convert_skill_100():
        skills_list = StoreHelper.load_data("position_profile_skills.dat", [])
        skills_convert_dict = {}
        prefered_list = ["analysis", "python", "r", "analytics", "machine learning", "sql", "modeling", "big data",
                         "hadoop", "java", "statistics", "mathematics", "sas", "data mining", "processing", "spark",
                         "security", "visualization", "testing", "c", "access", "optimization", "hive", "integration",
                         "excel", "tableau", "scripting", "development", "scala", "matlab", "linux", "nosql",
                         "management", "intelligence", "aws", "regression", "spss", "pig", "clustering", "saas",
                         "oracle", "go", "physics", "classification", "javascript", "operations research", "mapreduce",
                         "forecasting", "engineering", "powerpoint", "automation", "b2b", "segmentation", "dashboard",
                         "computing", "deep learning", "defense", "unix", "hbase", "d3", "perl", "algorithms",
                         "advertising", "word", "communication", "simulation", "data collection", "hardware", "command",
                         "apache", "troubleshooting", "ruby", "mongodb", "mysql", "probability", "hdfs", "econometrics",
                         "data warehousing", "scrum", "cassandra", "databases", "git", "cluster",
                         "statistical software", "manufacturing", "improvement", "pricing", "data architecture",
                         "critical thinking", "html", "design", "strategy", "fraud", "microsoft office", "teradata",
                         "quality assurance", "data integration", "experimentation", "customer service",
                         "bioinformatics"]
        for key in prefered_list:
            match = False
            if key not in skills_list:
                for skill in skills_list:
                    if key in skill:
                        match = True
                        if skill not in skills_convert_dict:
                            skills_convert_dict[skill] = key
                        else:
                            print ("%s key duplicate" % skill)
                        break
            else:
                match = True
                skills_convert_dict[key] = key
            if not match:
                print (key)
        StoreHelper.store_data(skills_convert_dict, 'skills_convert_dict.dat')
        print (len(skills_convert_dict))

    @staticmethod
    def generate_feature_vector(feature, profile_list, position_list):
        print ("Totally have %d profile" % len(profile_list))
        print ("Totally have %d position post" % len(position_list))

        print ("step 1, get fully set of this feature")
        profile_phrase_list = []
        for profile in profile_list:
            profile_phrase_list.extend(profile[feature])
        profile_phrase_list = list(set(profile_phrase_list))
        print ("Totally get %d words in profile for feature %s" % (len(profile_phrase_list), feature))
        position_phrase_list = []
        for position in position_list:
            if feature in position:
                position_phrase_list.extend(position[feature])
        position_phrase_list = list(set(position_phrase_list))
        print ("Totally get %d words in position for feature %s" % (len(position_phrase_list), feature))

        print ("step 2, generate full sum")
        phrase_list = list(set(profile_phrase_list).union(set(position_phrase_list)))
        print ("Totally get %d words in all for feature %s" % (len(phrase_list), feature))
        StoreHelper.store_data(phrase_list, "position_profile_%s.dat" % feature)

        print ("step 3, generate sum value")
        profile_sum = [0 for i in range(len(phrase_list))]
        position_sum = [0 for i in range(len(phrase_list))]
        for i in range(len(phrase_list)):
            for profile in profile_list:
                if phrase_list[i] in profile[feature]:
                    profile_sum[i] += 1
            for position in position_list:
                if feature in position and phrase_list[i] in position[feature]:
                    position_sum[i] += 1
        max_distance = DistanceHelper.compute_distance([i * 1.0 / len(profile_list) for i in profile_sum],
                                                       [i * 1.0 / len(position_list) for i in position_sum])
        csv_column = [feature, "total number"]
        csv_column.extend(phrase_list)
        csv_data = [["profile", len(profile_list)], ["position", len(position_list)]]
        csv_data[0].extend([str(i) for i in profile_sum])
        csv_data[1].extend([str(i) for i in position_sum])
        CsvHelper.write_list_to_csv("sum_%s.csv" % feature, csv_column, csv_data, sort_data_row=0, escape_first=2,
                                    append_rows=[['cross distance', max_distance]])
        return phrase_list, profile_sum, position_sum

    @staticmethod
    def get_profile_position_match():
        feature_list = ['years', 'education', 'major', 'skills']
        profile_vector = StoreHelper.load_data('profile_vector_common.dat', [])
        position_vector = StoreHelper.load_data('position_vector_common.dat', [])
        match_matrix = [[] for i in range(len(position_vector))]
        total_position = len(position_vector)
        for i in range(total_position):
            print("working on post %d totally %d" % (i, total_position))
            for profile in profile_vector:
                match_matrix[i].append(Main.generate_match_ratio_simple(position_vector[i], profile, feature_list))
        StoreHelper.store_data(match_matrix, 'position_profile_match_matrix.data')

    @staticmethod
    def generate_summary():
        position_profile_match_matrix = StoreHelper.load_data('position_profile_match_matrix.data', [])
        position_number = len(position_profile_match_matrix)
        profile_number = len(position_profile_match_matrix[0])
        index_dict = StoreHelper.load_data('index_dict.dat', {})
        test_cases = [(['major', 'education', 'years'], 0),
                      (['major', 'education', 'years', 'skills'], 0.1),
                      (['major', 'education', 'years', 'skills'], 0.2),
                      (['major', 'education', 'years', 'skills'], 0.3),
                      (['major', 'education', 'years', 'skills'], 0.4),
                      (['major', 'education', 'years', 'skills'], 0.5)]

        print ("Generate position perspective summary")
        csv_header = ["job post"]
        csv_data = None
        for test in test_cases:
            print("working on %s" % str(test))
            if test[1] > 0:
                csv_header.append(' '.join(test[0]) + "(%f)" % test[1])
            else:
                csv_header.append(' '.join(test[0]))
            if csv_data is None:
                csv_data = [[index_dict[i]] for i in range(position_number)]
            print (csv_data)
            for i in range(position_number):
                csv_data[i].append(sum([1 if match_rate > test[1] else 0 for match_rate in position_profile_match_matrix[i]]))
        CsvHelper.write_list_to_csv("position_perspective.csv", csv_header, csv_data)

        print ("Generate profile perspective summary")
        csv_header = ["profile"]
        csv_data = None
        for test in test_cases:
            print("working on %s" % str(test))
            if test[1] > 0:
                csv_header.append(' '.join(test[0]) + "(%f)" % test[1])
            else:
                csv_header.append(' '.join(test[0]))
            if csv_data is None:
                csv_data = [[i] for i in range(profile_number)]
            print (csv_data)
            for i in range(profile_number):
                csv_data[i].append(
                    sum([1 if position_profile_match_matrix[row][i] > test[1] else 0 for row in range(position_number)]))
        CsvHelper.write_list_to_csv("profile_perspective.csv", csv_header, csv_data)

    @staticmethod
    def convert_company(company_list):
        fortune_500 = CsvHelper.get_fortune_500_dict()
        count = 0
        total = len(company_list)
        # us_list_company_dict = StoreHelper.load_data('./resource/company_list.dat', {})
        convert_dict = {}
        for company in company_list:
            convert_value = DictHelper.find_in_key(fortune_500, company)
            if convert_value is not None:
                convert_dict[company] = convert_value
            count += 1
            print ("Total company %d now convert %d" % (total, count))
        return convert_dict

    @staticmethod
    def generate_convert_dict_1():
        convert_dict = {}
        position_company_dict = StoreHelper.load_data('company_name.dic')
        print (position_company_dict.keys())
        print (len(position_company_dict))
        print ("Filter Data Scientist Position!")
        position_scientist_dict = {}
        for i in range(8535):
            text_file = "./data/clean_post_lemmatize/%04d.dat" % i
            if StoreHelper.is_file_exist(text_file) and i in position_company_dict:
                position_scientist_dict[i] = position_company_dict[i]
        print ("After filter, contain position %d" % len(position_scientist_dict))
        position_scientist_dict = {index: company.lower() for index, company in position_scientist_dict.items()}
        StoreHelper.store_data(position_scientist_dict, 'position_scientist.dict')
        print ("Sample: %s" % str(random.sample(position_scientist_dict.values(), 3)))
        distinct_position_list = list(set(position_scientist_dict.values()))
        print (len(distinct_position_list))
        # distinct_position_list = [SegmentHelper.normalize(company) for company in distinct_position_list]
        convert_dict = Main.convert_company(distinct_position_list)
        print ("Get convert dict %d" % len(convert_dict))

        profile_list = StoreHelper.load_data('./resource/United States/profile.dat', [])
        profile_company_dict = {i: profile_list[i]['company'] for i in range(len(profile_list))}
        new_profile_dict = {}
        for index, company_list in profile_company_dict.items():
            company_list = [company.lower() for company in company_list]
            new_profile_dict[index] = company_list
        profile_company_dict = new_profile_dict
        print (len(profile_company_dict))
        print ("Sample: %s" % str(random.sample(profile_company_dict.values(), 3)))
        StoreHelper.store_data(profile_company_dict, 'profile_company.dict')
        profile_company_list = []
        for company_list in profile_company_dict.values():
            profile_company_list.extend(company_list)
        distinct_profile_list = list(set(profile_company_list))
        print ("After filter, contain position %d" % len(distinct_profile_list))
        distinct_profile_list = [company.lower() for company in distinct_profile_list]
        DictHelper.update_dict(convert_dict, Main.convert_company(distinct_profile_list))
        print ("Get convert dict %d" % len(convert_dict))
        StoreHelper.store_data(convert_dict, "convert_company.dic")

        csv_header = ['origin key', 'mapping key']
        csv_data = []
        for key, value in convert_dict.items():
            csv_data.append([key, value])
        CsvHelper.write_list_to_csv('company_convert_dict.csv', csv_header, csv_data)

    @staticmethod
    def convert_comapny_names_2():
        position_scientist_dict = StoreHelper.load_data('position_scientist.dict', {})
        profile_company_dict = StoreHelper.load_data('profile_company.dict', {})
        convert_dict = StoreHelper.load_data("convert_company.dic", {})

        position_scientist_dict = {index: DictHelper.get_key(convert_dict, company) for index, company in position_scientist_dict.items()}
        StoreHelper.store_data(position_scientist_dict, 'position_scientist.dict')

        profile_company_dict_new = {}
        for index, company_list in profile_company_dict.items():
            new_list = []
            for company in company_list:
                new_list.append(DictHelper.get_key(convert_dict, company))
            profile_company_dict_new[index] = new_list
        StoreHelper.store_data(profile_company_dict_new, 'profile_company.dict')

    @staticmethod
    def generate_company_summary_3():
        position_scientist_dict = StoreHelper.load_data('position_scientist.dict', {})
        profile_company_dict = StoreHelper.load_data('profile_company.dict', {})
        company_summary_dict = {}
        for index, company in position_scientist_dict.items():
            if company not in company_summary_dict:
                company_summary_dict[company] = [[], []]
            company_summary_dict[company][0].append(index)
        for index, company_list in profile_company_dict.items():
            for company in company_list:
                if company not in company_summary_dict:
                    company_summary_dict[company] = [[], []]
                company_summary_dict[company][1].append(index)
        StoreHelper.store_data(company_summary_dict, 'company_summary.dict')
        company_count = {company: (len(count_list[0]) + len(count_list[1])) for company, count_list in company_summary_dict.items()}
        StoreHelper.save_file(DictHelper.get_sorted_list(company_count), 'company_summary.txt')

    @staticmethod
    def clean_summary_4():
        company_summary_dict = StoreHelper.load_data('company_summary.dict', {})
        # company_summary_dict = {company.strip(): details for company, details in company_summary_dict.items()}
        # del company_summary_dict['research']
        # del company_summary_dict['consulting']
        # del company_summary_dict['ai']
        # del company_summary_dict['college']
        # del company_summary_dict['open']
        # del company_summary_dict['university of']
        # del company_summary_dict['data scientist']
        # del company_summary_dict['finance']
        # del company_summary_dict['industry']
        StoreHelper.store_data(company_summary_dict, 'company_summary.dict')
        company_count = {company: (len(count_list[0]) + len(count_list[1])) for company, count_list in
                         company_summary_dict.items()}
        StoreHelper.save_file(DictHelper.get_sorted_list(company_count), 'company_summary.txt')

    @staticmethod
    def generate_output_5():
        company_summary_dict = StoreHelper.load_data('company_summary.dict', {})
        fortune_500 = CsvHelper.get_fortune_500_dict()
        company_dict = {}
        for company, details in company_summary_dict.items():
            if company in fortune_500:
                if fortune_500[company] < 100:
                    DictHelper.append_dic_key(company_dict, 2, (company, details))
                else:
                    DictHelper.append_dic_key(company_dict, 1, (company, details))
            else:
                DictHelper.append_dic_key(company_dict, 0, (company, details))
        StoreHelper.store_data(company_dict, 'rank-company_posts_profiles.dic')
        # sorted_list = DictHelper.get_sorted_list(company_dict, sorted_by_key=True)
        # csv_header = ['company type(2: first 100, 1: first 500, 0: not in fortune list', 'company name', 'position', 'profile']
        # csv_data = []
        # count_list = []
        # for company, details in company_dict[2]:
        #     csv_data.append([2, company, str(details[0]), str(details[1])])
        #     count_list.extend(details[1])
        # print ("Type 2 total count: %d" % len(count_list))
        # count_list = []
        # for company, details in company_dict[1]:
        #     csv_data.append([1, company, str(details[0]), str(details[1])])
        #     count_list.extend(details[1])
        # print ("Type 1 total count: %d" % len(count_list))
        # for company, details in company_dict[0]:
        #     csv_data.append([0, company, str(details[0]), str(details[1])])
        # CsvHelper.write_list_to_csv('type_company_summary.csv', csv_header, csv_data)

    @staticmethod
    def generate_job_post_meet_summary(perspective=None):
        test_cases = [(['major', 'education', 'years'], 0),
                      (['major', 'education', 'years', 'skills'], 0.1),
                      (['major', 'education', 'years', 'skills'], 0.2),
                      (['major', 'education', 'years', 'skills'], 0.3),
                      (['major', 'education', 'years', 'skills'], 0.4),
                      (['major', 'education', 'years', 'skills'], 0.5)]
        csv_header = ["job post"]
        csv_data = None
        for test in test_cases:
            if test[1] > 0:
                csv_header.append(' '.join(test[0]) + "(%f)" % test[1])
            else:
                csv_header.append(' '.join(test[0]))
            if perspective is None or perspective == 'position':
                meet_dict = Main.find_position_candidate(None, 0.99, test[0], test[1])
            elif perspective == 'profile':
                meet_dict = Main.find_profile_candidate(None, 0.99, test[0], test[1])
            print (meet_dict)
            if csv_data is None:
                csv_data = [[key] for key in meet_dict]
            print (csv_data)
            for row in csv_data:
                row.append(meet_dict[row[0]])
        CsvHelper.write_list_to_csv("position_perspective.csv", csv_header, csv_data)


if __name__ == '__main__':
    # Main.cross()
    # Main.generate_profile_position_common()
    # Main.generate_job_post_meet_summary()
    # Main.find_profile_candidate(1, 0.9)
    # Main.get_profile_position_match()
    # Main.generate_convert_dict_1()
    # Main.convert_comapny_names_2()
    # Main.generate_company_summary_3()
    Main.generate_output_5()




