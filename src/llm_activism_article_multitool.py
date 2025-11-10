import json
import html
import re
import datetime
import glob
import os
import warnings
import random
import sys
import llmproc_core as llm
import llm_activism_article_prompts_and_strings as pas
import atexit
import math
import subprocess
import msvcrt  # For Windows key press detection
import time
import csv
import copy

debug_log = False
debug_file_handle = open("debug_log.txt", 'w', encoding='utf-8')

def cleanup():
    global debug_file_handle
    if debug_file_handle is not None:
        debug_file_handle.close()
        debug_file_handle = None
atexit.register(cleanup)

def write_debug(message: str) -> None:
    time_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_file_handle.write(f"{time_now} {message}\n\n")
    debug_file_handle.flush()

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

warning_log_filename = f"warnings_{timestamp}.log"

def custom_formatwarning(message, category, *_args, **_kwargs ):
    formatted_warning = f"{datetime.datetime.now()}: {category.__name__}: {message}\n"
    with open(warning_log_filename, 'a') as log_file:
        log_file.write(formatted_warning)
    return formatted_warning

warnings.formatwarning = custom_formatwarning

coding_form = None

def read_coding_form( coding_form_file = "protestCharacteristicForm.tsv" ):
    global coding_form
    with open( coding_form_file, 'r') as coding_form_file:
        coding_form = coding_form_file.read()

def load_config(config_file_path: str):
    try:
        with open(config_file_path, 'r') as file:
            config = json.load(file)
        articles_path = config.get('articles_path', "INPUT_article_contents")
        do_screening = config.get('do_screening', False)
        do_coding = config.get('do_coding', False)
        do_summarising = config.get('do_summarising', False)
        process_only_selected = config.get('process_only_selected', False)
        stop_after = config.get('stop_after', 1)
        count_type = config.get('count_type', "pass_screening")
        article_order_random_seed = config.get('article_order_seed', 420)
        output_article_full = config.get('output_article_full', False)
        output_article_summarised = config.get('output_article_summarised', False)
        output_article_summary_process = config.get('output_article_summary_process', False)
        output_only_articles_passing_screening = config.get('output_only_articles_passing_screening', False)
        output_detailed_word_counts = config.get('output_detailed_word_counts', False)
        article_selection = config.get('article_selection', "random")
        article_exclusion_list = config.get('article_exclusion_list', "none")
        output_picture_tags = config.get('output_picture_tags', False )
        coding_output_filename = config.get('coding_output_filename', f"output_folders/coding_output/coding_output_{timestamp}.tsv" )
        html_output_filename = config.get('html_output_filename', f"output_folders/article_HTML_output/formatted_articles_{timestamp}.tsv")

        if do_coding and not do_screening:
            warnings.warn("Not tested: do_screening false with do_coding true.", UserWarning)
        if do_summarising and not do_screening:
            warnings.warn("do_summarising without do_screening could result in strange summaries for articles that don't pass screening.", UserWarning)
        if ( output_article_summarised or output_article_summarised ) and not do_summarising:
            warnings.warn("Summary output requested without summary.", UserWarning)
        return articles_path, do_screening, do_coding, do_summarising, process_only_selected, stop_after, count_type, article_order_random_seed, output_article_full, output_article_summarised, output_article_summary_process, output_only_articles_passing_screening, output_detailed_word_counts, article_selection, article_exclusion_list, output_picture_tags, coding_output_filename, html_output_filename
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file_path}")
        raise
    except json.JSONDecodeError:
        print(f"Invalid JSON format in configuration file: {config_file_path}")
        raise
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        raise

def count_words(text):
    if text is None: return 0
    return len(text.split())

def get_title_and_subtitle_and_article(article, body):
    return article["title"] + "\n" + (article["subtitle"] + "\n" if article["subtitle"] else "") + body

def tsv_extract_column(tsv_string: str, index: int) -> str:
    index = index - 1 # So it can be called using 1-based indexing
    lines = tsv_string.strip().split('\n')
    column = []
    for line in lines:
        parts = line.split('\t')
        if index < len(parts):
            column.append(parts[index])
        else:
            raise IndexError(f"Column index {index} is out of range for line: {line}")
    return '\n'.join(column)

def tsv_column_bind(tsv_string1: str, tsv_string2: str) -> str:
    lines1 = tsv_string1.strip().split('\n')
    lines2 = tsv_string2.strip().split('\n')
    if len(lines1) != len(lines2):
        raise ValueError("Both input TSV strings must have the same number of rows.")
    result = []
    for line1, line2 in zip(lines1, lines2):
        result.append(f"{line1}\t{line2}")
    return '\n'.join(result)

def tsv_merge_two_and_two_columns_and_check(tsv_string1: str, tsv_string2: str) -> str:
    lines1 = tsv_string1.strip().split('\n')
    lines2 = tsv_string2.strip().split('\n')
    if len(lines1) != len(lines2):
        raise ValueError("The two TSV strings have different numbers of rows.")
    merged_lines = []
    for line1, line2 in zip(lines1, lines2):
        cols1 = line1.split('\t')
        cols2 = line2.split('\t')
        if len(cols1) != 2 or len(cols2) != 2:
            raise ValueError("Each line must have exactly two columns in both strings.")
        if cols1[0] != cols2[0]:
            raise ValueError("Non-matching row-name columns.")
        match_status = 'match' if cols1[1] == cols2[1] else 'MISMATCH'
        merged_line = f"{cols1[0]}\t{cols1[1]}\t{cols2[1]}\t{match_status}"
        merged_lines.append(merged_line)
    return '\n'.join(merged_lines)

def replace_question_names_with_full_questions(comparison):
    questions = tsv_extract_column(coding_form, 3)
    questions = '\n'.join(questions.split('\n')[1:]) # coding form has header column but LLM output doesn't
    answers1 = tsv_extract_column(comparison, 2)
    answers2 = tsv_extract_column(comparison, 3)
    match = tsv_extract_column(comparison, 4)
    return tsv_column_bind(questions, tsv_column_bind(answers1, tsv_column_bind(answers2,match)))

def sanitise_name(filename):
    # Remove or replace characters that are problematic in filenames
    # Keep alphanumeric characters, dots, hyphens, and underscores
    sanitized = re.sub(r'[^\w\-._]', '_', filename)
    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip('. ')
    # Collapse multiple underscores into a single underscore
    sanitized = re.sub(r'__+', '_', sanitized)
    return sanitized

def sanitise_ids(articles):
    # Create a copy to avoid modifying the original
    sanitized_articles = articles.copy()
    seen_ids = set()
    duplicates_found = False
    # Sanitize IDs and remove duplicates in a single pass
    article_ids_to_remove = []
    for article_id, article in list(sanitized_articles.items()):
        if article.get("id") is None: continue
        original_id = article['id']
        sanitized_id = sanitise_name(original_id)
        if sanitized_id in seen_ids:
            # Remove this article as it has a duplicate ID
            article_ids_to_remove.append(article_id)
            duplicates_found = True
        else:
            seen_ids.add(sanitized_id)
            # Update the ID immediately
            article['id'] = sanitized_id
    # Remove the articles with duplicate IDs
    for article_id in article_ids_to_remove:
        del sanitized_articles[article_id]
    # Warn once if duplicates were found and removed
    if duplicates_found:
        warnings.warn("Warning: some articles with duplicate IDs were removed.", UserWarning)
    return sanitized_articles

def do_summarisation_for_article(article, do_coding, very_short_summary, check_summary, do_summary_corrections, llm_correction_instructions_dict):
    if article["text_word_count"] > 350 or very_short_summary:
        article["summary"] = summarise_article_via_cache(article, very_short_summary)
        article["summarised"] = True
        article["summary_word_count"] = count_words(article["summary"])
        if check_summary:
            article["summary_check"] = do_summary_check_via_cache(article)
        if do_coding:
            article["summary_coded"] = code_article(article, "summary")
            article["summary_comparison"] = tsv_merge_two_and_two_columns_and_check(article["codes_string"], article["summary_coded"])
            if False or "MISMATCH" in tsv_extract_column(article["summary_comparison"],4): # Never re-summarising anyway using the legacy system (for now) for convenience
                print("Re-summarising")
                article["legacy_resummarised"] = "Yes"
                article["legacy_resummary"] = legacy_resummarise_article(article)
                article["legacy_resummary_word_count"] = count_words(article["legacy_resummary"])
                article["legacy_resummary_coded"] = code_article(article, "legacy_resummary")
                article["legacy_resummary_comparison"] = tsv_merge_two_and_two_columns_and_check(article["codes_string"], article["legacy_resummary_coded"])
            else:
                article["legacy_resummarised"] = "No"
        if do_summary_corrections:
            article_id = article["id"]
            if article_id in llm_correction_instructions_dict:
                article["correction_instructions"] = llm_correction_instructions_dict[article_id]
                article["corrected_summary"] = do_summary_correction_via_cache(article)
                article["corrected_summary_word_count"] = count_words(article["corrected_summary"])
                article["has_corrected_summary"] = True
            else:
                article["has_corrected_summary"] = False
                article["correction_instructions"] = ""
        else:
            article["has_corrected_summary"] = False
            article["correction_instructions"] = ""
    else:
        article["summarised"] = False
        article["has_corrected_summary"] = False
        article["correction_instructions"] = ""
        if do_summary_corrections and article["id"] in llm_correction_instructions_dict:
            print(f"ERROR: Article {article['id']} has correction instructions but does not meet criteria for summarisation")
            sys.exit(1)

def summarise_article(article, very_short_summary):
    content = "TITLE: " + article["title"] + "\n" + article["subtitle"] + "\n" + article["text"]
    if very_short_summary:
        prompt = pas.prompt_summarise_very_short_intro + content + pas.prompt_summarise_end
    else:
        prompt = pas.prompt_summarise_intro + content + pas.prompt_summarise_end
    response = llm.send_prompt(prompt, "summariser", article["title"])
    if response.startswith(article["title"]):
        return response[len(article["title"]):].lstrip()
    else:
        raise ValueError("The summary did not begin with the article title.")

def summarise_article_via_cache(article, very_short_summary):
    return llm.process_with_cache( summarise_article, article, very_short_summary )

def do_summarisation_check(article):
    content = "ORIGINAL ARTICLE\n\n" + "TITLE: " + article["title"] + "\n" + article["subtitle"] + "\n" + article["text"] + "\n\nSUMMARISED ARTICLE\n\n" + "TITLE: " + article["title"] + "\n" + article["subtitle"] + "\n" + article["summary"]
    prompt = pas.prompt_check_summary_intro + content + pas.prompt_check_summary_end
    response = llm.send_prompt(prompt, "processor")
    if response.startswith( ("pass", "consistency_issue", "form_issue", "new_material_issue", ) ):
        response = re.sub(r'\s+', ' ', response).strip()
        return response
    else:
        raise ValueError(f"Summary check response malformed: {response}")

def do_summary_check_via_cache(article):
    return llm.process_with_cache(do_summarisation_check, article)

def do_summary_correction_via_cache(article):
    return llm.process_with_cache(do_summary_correction, article)

def do_summary_correction(article):
    content = f"""ORIGINAL ARTICLE

    TITLE: {article['title']}
    SUBTITLE: {article.get('subtitle', '')}
    TEXT: {article['text']}

    SUMMARISED ARTICLE

    TITLE: {article['title']}
    SUBTITLE: {article.get('subtitle', '')}
    TEXT: {article['summary']}

    CORRECTIONS NEEDED

    {article['correction_instructions']}
    """
    prompt = pas.prompt_correct_summary_intro + content + pas.prompt_correct_summary_end
    response = llm.send_prompt(prompt, "summariser")
    return response

def legacy_resummarise_article(article):
    if article["summary_word_count"] < 350:
        word_count_prompt = "The maximum word count for the resummarised article is 350 words.\n"
    else:
        word_count_prompt = "The resummarised article may not increase in length. If you add new material from the original article, you must also remove material.\n"
    comparison_with_full_questions = replace_question_names_with_full_questions( article["summary_comparison"] )
    prompt = ( pas.prompt_legacy_resummarise_intro + article["text"] + pas.prompt_legacy_resummarise_link1 + article["summary"] + pas.prompt_legacy_resummarise_link2 +
               comparison_with_full_questions + pas.prompt_legacy_resummarise_end + word_count_prompt )
    return llm.send_prompt( prompt, "summariser" )

def owe_focussed(article):
    title_and_body = get_title_and_subtitle_and_article(article, article["text"])
    prompt = pas.prompt_owe_intro + title_and_body + pas.prompt_owe_end
    yes_or_no = llm.send_prompt( prompt, "processor" )
    if yes_or_no.startswith("Yes") and (len(yes_or_no) == 3 or yes_or_no[3:4].isspace()):
        yes_or_no = "Yes"
    elif yes_or_no.startswith("No") and (len(yes_or_no) == 2 or yes_or_no[2:3].isspace()):
        yes_or_no = "No"
    if yes_or_no != "Yes" and yes_or_no != "No":
        print(f"This is not Yes or No: {yes_or_no}")
        raise ValueError("Bad response for owe check.")
    if debug_log:
        write_debug(f"owe_focussed() for {article['id']}\nPROMPT: {prompt}\n\nRESPONSE: {yes_or_no}\n")
    return yes_or_no

def owe_focussed_via_cache(article):
    return llm.process_with_cache( owe_focussed, article )

def owe_specific(article):
    title_and_body = get_title_and_subtitle_and_article(article, article["text"])
    prompt = pas.prompt_owe_specific_intro + title_and_body + pas.prompt_owe_specific_end
    yes_or_no = llm.send_prompt(prompt, "processor")
    if yes_or_no != "Yes" and yes_or_no != "No":
        print("yes_or_no was ", yes_or_no)
        raise ValueError("Bad response for owe specific check.")
    if debug_log:
        write_debug(f"owe_specific() for {article['id']}\nPROMPT: {prompt}\n\nRESPONSE: {yes_or_no}\n")
    return yes_or_no

def owe_specific_via_cache(article):
    return llm.process_with_cache(owe_specific, article)

def parse_and_validate_screening_response(response):
    lines = response.strip().split('\n')
    if len(lines) != 2:
        raise ValueError("Response must contain exactly two lines")
    headers = lines[0].split('\t')
    values = lines[1].split('\t')
    if len(headers) != len(values) or len(headers) != len(pas.screening_code_names):
        raise ValueError(f"Number of fields in response doesn't match pas.screening_code_names {len(headers)} {len(values)} {len(headers)}{len(pas.screening_code_names)}")
    if set(headers) != set(pas.screening_code_names):
        raise ValueError("Headers in response don't match pas.screening_code_names keys")
    if not all(value in ['Yes', 'No'] for value in values):
        raise ValueError("All values must be either 'Yes' or 'No'")
    screening_codes = {}
    for header, value in zip(headers, values):
        screening_codes[header] = value
    return screening_codes

def prompt_llm_with_categorisation_message_with_prefill(prompt, prefill):
    return llm.send_prompt( prompt, "processor", prefill )

def full_screening(article):
    title_and_body = get_title_and_subtitle_and_article(article, article["text"])
    prompt = pas.prompt_full_screening_intro + title_and_body + pas.prompt_full_screening_end
    prefill = "\t".join(pas.screening_code_names)
    response = llm.send_prompt( prompt, "processor", prefill )
    if debug_log:
        write_debug(f"full_screening() for {article['id']}\nPROMPT: {prompt}\n\nRESPONSE: {response}\n")
    return parse_and_validate_screening_response(response)

def full_screening_via_cache(article):
    return llm.process_with_cache( full_screening, article )

def code_article(article, version):
    title_and_body = get_title_and_subtitle_and_article(article, article[version])
    prompt = pas.prompt_coding_intro + coding_form + pas.prompt_coding_link + title_and_body + pas.prompt_coding_end
    prefill = "Number of protestors"
    response = llm.send_prompt(prompt, "processor", prefill)
    code_names_string = tsv_extract_column(response,1)
    code_names = [line.strip() for line in code_names_string.splitlines()]
    if code_names != pas.rating_code_names:
        raise ValueError("LLM did not return correct code names.")
    codes_string = tsv_extract_column(response,2)
    codes_list = [line.strip() for line in codes_string.splitlines()]
    article["codes_"+version] = dict(zip(code_names, codes_list))
    return response

def format_html_body_text(text,breaks_number="single"):
    breaks = "<br>" if breaks_number == "single" else "<br><br>"
    text = text.replace('\n\n', '\n')
    processed_text = html.escape(text).replace('\n', breaks).replace('\\"', '&quot;')
    return f"<p>{processed_text}</p>"

def make_html_table(text, header):
    html_output = "<table border='1'>"
    html_output += header
    for row in text.split('\n'):
        cells = row.split('\t')
        html_output += "<tr>"
        for cell in cells:
            html_output += f"<td>{html.escape(cell)}</td>"
        html_output += "</tr>"
    html_output += "</table>"
    return html_output

def produce_output_summary_process_html(article):
    html_output = "<html><body>"
    html_output += f"<h1>{article['title']}</h1>"
    html_output += "<h2>Original:</h2>" + format_html_body_text(article["text"])
    html_output += f"<p>Word count: {article['text_word_count']}</p>"
    if article["summarised"]:
        html_output += "<h2>Summary:</h2>"
        html_output += format_html_body_text(article["summary"])
        html_output += f"<p>Summary word count: {article['summary_word_count']}</p>"
        if article["legacy_resummarised"] == "Yes":
            html_output += "<h2>Resummary:</h2>"
            html_output += format_html_body_text(article["legacy_resummary"])
            html_output += f"<p>Resummary word count: {article['legacy_resummary_word_count']}</p>"
            html_output += "<h2>Original, summary and resummary coding comparison:</h2>"
            html_output += make_html_table(compare_summary_and_legacy_resummary_matches(article), "<tr><th>Question</th><th>Original</th><th>Summary</th><th>Match</th><th>Resummary</th><th>Match</th></tr>")
        else:
            html_output += "<h2>Original and summary coding comparison:</h2>"
            html_output += make_html_table(article["summary_comparison"], "<tr><th>Question</th><th>Original</th><th>Summary</th><th>Match</th></tr>")
    else:
        html_output += "<h2>Coding:</h2>"
        html_output += make_html_table(article["codes_string"], "<tr><th>Question</th><th>Code</th></tr>")
    html_output += "</body></html>"
    return html_output

def compare_summary_and_legacy_resummary_matches( article ):
    questions = tsv_extract_column(article["summary_comparison"], 1)
    original_answers = tsv_extract_column(article["summary_comparison"], 2)
    summary_answers = tsv_extract_column(article["summary_comparison"], 3)
    summary_match = tsv_extract_column(article["summary_comparison"], 4)
    legacy_resummary_answers = tsv_extract_column(article["legacy_resummary_comparison"], 3)
    legacy_resummary_match = tsv_extract_column(article["legacy_resummary_comparison"], 4)
    return tsv_column_bind(questions, tsv_column_bind(original_answers, tsv_column_bind(summary_answers, tsv_column_bind(summary_match, tsv_column_bind(legacy_resummary_answers,legacy_resummary_match)))))

#countNoIDs = 0

def prepare_articles(articles):
    #global countNoIDs
    for url, article in articles.items():
        article["url"] = url
        article["passes_screening"] = None
        article["summarised"] = False
        if "id" not in article:
            #countNoIDs += 1
            #print("Articles with no ID: " + str(countNoIDs))
            pattern = r'article-(\d+)\/([a-zA-Z0-9]+)-([a-zA-Z0-9]+)-([a-zA-Z0-9]+)'
            match = re.search(pattern, url)
            if match:
                id_code = match.group(1) + '-' + '-'.join(match.group(2, 3, 4))
                article["id"] = id_code
                warnings.warn( f"Article '{article['url']}' has no ID, substituting {id_code} which will only work well for certain Daily Mail articles", UserWarning)
            else: #The reason there are two different methods for constructing IDs when they are missing is originally they could only be Daily Mail articles, and I made a method that worked for them. Then some non-Daily Mail ones turned up (in a new scrape) and I needed a new method that works for these ones, while keeping the old method for the ones it worked on, so we don't end up with two IDs for the same article
                article["id"] = article["url"].split('://', 1)[1].replace('/', '_').replace(':', '_').replace('.','_').replace('?', '_').replace('&', '_')
                #warnings.warn(f"Article '{article['url']}' has no ID, substituting {article["id"]}", UserWarning)
        if "source" not in article:
            article["source"] = "Daily-Mail"
            warnings.warn( f"Article '{article['id']}' has no source, assuming Daily Mail", UserWarning)
        if article["subtitle"] is None:
            article["subtitle"] = ""
        # Strip problematic Unicode whitespace characters that have been known to occur
        article["title"] = article["title"].replace('\u2028', ' ').replace('\u2029', ' ')
        if article["subtitle"]:
            article["subtitle"] = article["subtitle"].replace('\u2028', ' ').replace('\u2029', ' ')
        article["text"] = article["text"].replace('\u2028', ' ').replace('\u2029', ' ')
        article["long_subtitle_to_body"] = False
        article["text_word_count"] = count_words(article["text"])
        article["title_word_count"] = count_words(article["title"])
        article["subtitle_word_count"] = count_words(article["subtitle"])
        if (article["subtitle_word_count"]) >= 50:
            article["long_subtitle_to_body"] = True
            article["text"] = article["subtitle"] + "\n" + article["text"]
            article["subtitle"] = ""
            article["text_word_count"] = count_words(article["text"])
            article["subtitle_word_count"] = count_words(article["subtitle"])
    correct_specific_scraping_issues(articles)

def correct_specific_scraping_issues(articles):
    for url, article in articles.items():
        article_id = article.get("id")
        # BBC_2024-04-06: Missing pictures
        if article_id == "BBC_2024-04-06_Greta-Thunberg-Activist-arrested":
            article["image"] = [
                {
                    "url": "https://ichef.bbci.co.uk/news/1024/cpsprodpb/B567/production/_133093464_d98674f8e6e02b28ab34ef2a4267268ddaa551660_0_2694_15151000x563.jpg.webp",
                    "caption": ""
                },
                {
                    "url": "https://ichef.bbci.co.uk/news/1024/cpsprodpb/146B7/production/_133093638_bfaaf60d0dc788a63882eeb58e9ad6d4a948d58e0_510_4893_27521000x563.jpg.webp",
                    "caption": "Extinction Rebellion organisers say this is the 37th time they have protested on the A12 highway"
                },
                {
                    "url": "https://ichef.bbci.co.uk/news/1024/cpsprodpb/441F/production/_133093471_944de1a5e28f5379007482f285eca54c94734ad10_0_5272_29661000x563.jpg.webp",
                    "caption": "Greta Thunberg was loaded into a bus and driven away from the protest, along with fellow detainees"
                }
            ]
        # Two articles: Remove grey placeholder as middle picture
        if article_id == "BBC_2024-12-17_Climate-groups-to-back" or article_id == "BBC_2025-09-22_Arrests-after-gas-protesters":
            if article.get("image") and len(article["image"]) > 1:
                del article["image"][1]
        # BBC_2025-07-25: Correct third image URL
        if article_id == "BBC_2025-07-25_Forth-Road-Bridge-closed":
            article["image"][2]["url_large"] = "https://ichef.bbci.co.uk/news/1024/cpsprodpb/af50/live/0e2bb6b0-6963-11f0-b2d3-f75ba2a92ec7.jpg.webp"
        # Add missing image for BBC article
        if article_id == "BBC_2025-02-02_Protesters-block-airport-over":
            article["image"][1]["url_large"] = "https://ichef.bbci.co.uk/news/1024/cpsprodpb/51c2/live/1f798f30-e19d-11ef-9c5d-25d17bbea272.jpg.webp"
            article["image"][1]["caption"] = "Protesters are calling for a total ban on private jets"
        # Daily-Mail_2024-03-15: Invalid subtitle
        if article_id == "Daily-Mail_2024-03-15_Moment-Sopranos-star":
            if article.get("subtitle") == ".":
                article["subtitle"] = None

def screen_and_code_article(article, do_screening=True, do_coding=False, use_owe_focussed=True, use_owe_specific=False,get_owe_focussed_llm_coding=False):
    print(f"Processing {article['id']} word count " + str(article['text_word_count']))
    if article_has_image_issues(article):
        warnings.warn(f"Article being processed has image issues: {article['id']}", UserWarning)
    if do_screening:
        article["screening_codes"] = full_screening_via_cache(article)
        s_c = article["screening_codes"]
        if use_owe_focussed or get_owe_focussed_llm_coding:
            article["owe_focussed_llm"] = owe_focussed_via_cache(article)
            print("OWE FOCUSSED LLM is " + article["owe_focussed_llm"])
        else:
            article["owe_focussed_llm"] = "Unused"
        if use_owe_focussed:
            owe = article["owe_focussed_llm"]
        else:
            print("OWE is " + s_c["OWE"])
            owe = s_c["OWE"]
        if use_owe_specific:
            article["owe_specific_llm"] = owe_specific_via_cache(article)
            print("OWE SPECIFIC CODING KEPT BLIND")
            # print("OWE SPECIFIC is " + article["owe_specific_llm"])
        else:
            article["owe_specific_llm"] = "Unused"
            article["owe_specific_human"] = "Unused"
            article["passes_screening_specific"] = "Unused"
        if owe == "No" or s_c["LETTER"] == "Yes" or s_c["ROUNDUP"] == "Yes" or s_c["NON-UK EDITION"] == "Yes" or s_c["VIDEO"] == "Yes":
            article["passes_screening"] = "No"
        else:
            article["passes_screening"] = "Yes"
    if do_coding and article["passes_screening"] == "Yes":
        article["codes_string"] = code_article(article, "text")
    return True

def split_string_at_midpoint(input_string):
    lines = input_string.splitlines()
    total_length = sum(len(line) for line in lines)
    halfway_point = total_length // 2
    current_length = 0
    split_index = 0
    for i, line in enumerate(lines):
        current_length += len(line)
        if current_length >= halfway_point:
            split_index = i
            break
    first_part = '\n'.join(lines[:split_index + 1])
    second_part = '\n'.join(lines[split_index + 1:])
    return first_part, second_part

def article_has_image_issues(article):
    images = article["image"]
    if images:
        for image in images:
            if "local_name" not in image or image.get("local_name") is None:
                return True
    return False

def generate_image_html_old(article, image_data): # This one can't cope with the inconsistent paths
    github_image_root = "https://raw.githubusercontent.com/claravdw/disruption/refs/heads/main/content_scraping/"
    if "local_name" not in image_data or image_data.get("local_name") is None:
        #warnings.warn(f"Image for {image_data["url"]} has no local name", UserWarning)
        image_path = image_data["url"]
        article["scraped_image_missing"] = True
    else:
        image_path = github_image_root + image_data['local_name']
    caption = image_data['caption']
    image_html = f'''
    <figure width="100%">
      <img src="{image_path}" alt="{caption}" width="100%">
      <figcaption align="center">{caption}</figcaption>
    </figure>
    '''
    return image_html

def llm_describe_image(image_url):
    pass

def generate_image_html_github_url(article, image_data, output_picture_tags):
    github_image_root = "https://raw.githubusercontent.com/claravdw/disruption/refs/heads/main/content_scraping/"
    if type(image_data) is list:
        caption = image_data[0]
        image_path = image_data[1]
    else:
        if "local_name" not in image_data or image_data.get("local_name") is None:
            # warnings.warn(f"Image for {image_data["url"]} has no local name", UserWarning)
            image_path = image_data["url"]
            article["scraped_image_missing"] = True
        else:
            local_name = image_data['local_name']
            local_path = image_data.get('local_path', '')
            # Check if local_path is at the start of local_name
            if local_name.startswith(local_path):
                image_path = github_image_root + local_name
            else:
                # If not, combine local_path and local_name
                image_path = github_image_root + local_path + '/' + local_name
            # Remove any double slashes that might occur, except in https://
            image_path = re.sub(r'(?<!:)//+', '/', image_path)
        caption = image_data['caption']
    if output_picture_tags:
        pic_tag = "#PH"
        caption_start_tag = "#CS "
        caption_end_tag = " #CE"
        image_description = llm.process_url_with_cache(llm_describe_image,image_path)
    else:
        pic_tag = ""
        caption_start_tag = ""
        caption_end_tag = ""
    image_html = f'''
    <figure width="100%">
      {pic_tag}<img src="{image_path}" alt="{caption}" width="100%">
      {caption_start_tag}<figcaption align="center">{caption}</figcaption>{caption_end_tag}
    </figure>
    '''
    return image_html


def generate_image_html_outlet_url(article, image_data, output_picture_tags):
    # Get the image URL from the outlet
    if "url_large" in image_data:
        image_path = image_data["url_large"]
    elif "url" in image_data:
        image_path = image_data["url"]
    else:
        warnings.warn(f"Image for {article['id']} has neither url_large nor url", UserWarning)
        image_path = ""

    # Clean Telegraph URLs that have the /web/timestamp prefix
    if image_path and "telegraph.co.uk/web/" in image_path:
        match = re.search(r'https://www\.telegraph\.co\.uk/web/[^/]+/(https://.*)', image_path)
        if match:
            image_path = match.group(1)

    # NOTE: Intentionally NOT using GitHub URLs - we want outlet URLs
    # The local_name and local_path fields are ignored in this function

    caption = image_data.get('caption', '')

    if output_picture_tags:
        pic_tag = "#PH"
        caption_start_tag = "#CS "
        caption_end_tag = " #CE"
    else:
        pic_tag = ""
        caption_start_tag = ""
        caption_end_tag = ""

    image_html = f'''
    <figure width="100%">
      {pic_tag}<img src="{image_path}" alt="{caption}" width="100%">
      {caption_start_tag}<figcaption align="center">{caption}</figcaption>{caption_end_tag}
    </figure>
    '''
    return image_html

def formatted_article_output(article, output_summary=False, output_picture_tags=False,
                             suppress_id_in_html=False, pad_margins=True, complete_html=True, output_corrected_summary=False):
    identity_code, source, title, subtitle, images = article["id"], article["source"], article["title"], article[
        "subtitle"], article["image"]
    if output_corrected_summary:
        body = article["corrected_summary"]
    elif not output_summary:
        body = article["text"]
    else:
        body = article["summary"]
    image_strings = []
    if images:
        image_strings = [generate_image_html_outlet_url(article, image, output_picture_tags) for image in images]
        n_images = len(image_strings)
    else:
        n_images = 0
    if "scraped_image_missing" not in article:
        article["scraped_image_missing"] = False
    first_half, second_half = split_string_at_midpoint(body)
    if complete_html:
        if pad_margins:
            html_output = "<html><head><style>body { max-width: 800px; margin: 0 auto; padding: 20px; }</style></head><body><br>"
        else:
            html_output = "<html><head></head><body><br>"
    else:
        html_output = ""
    if not suppress_id_in_html:
        html_output += f"<h2>ID: {identity_code}</h2>"
    else:
        html_output += f"\n<!--Article ID: {identity_code}-->\n"
    html_output += f'''
          <img src="https://raw.githubusercontent.com/claravdw/disruption/refs/heads/main/content_scraping/outlet_logos/{source}.png" alt="Outlet logo" style="display: block; margin: 0 auto; width: 25%; min-width: 150px;">
        '''
    if output_picture_tags:
        html_output += f"<h1>Title: {title}</h1>"
    else:
        html_output += f"<h1>{title}</h1>"
    if bool(subtitle and subtitle.strip()):
        if output_picture_tags:
            html_output += f"<h2>Subtitle: {subtitle}</h2>"
        else:
            html_output += f"<h2>{subtitle}</h2>"
    if output_picture_tags:
        html_output += "Content: "
    match n_images:
        case 0 | 1:
            pass
        case _:
            html_output += image_strings[0]
    html_output += format_html_body_text(first_half, "double")
    match n_images:
        case 0:
            pass
        case 1:
            html_output += image_strings[0]
        case _:
            html_output += image_strings[1]
    formatted_second_half = format_html_body_text(second_half, "double")
    formatted_second_half = ("<p>" + formatted_second_half.removeprefix("<p><br><br>")) if formatted_second_half.startswith("<p><br><br>") else formatted_second_half
    html_output += formatted_second_half
    match n_images:
        case 0 | 1 | 2:
            pass
        case _:
            html_output += image_strings[2]
    if complete_html:
        html_output += "</body></html>"
    return html_output

def start_side_by_side_html(filename):
    html_header = """<html>
<head>
<style>
body { 
    margin: 20px;
    font-family: Arial, sans-serif;
}
table {
    width: 100%;
    border-collapse: collapse;
}
th {
    width: 33.33%;
    padding: 10px;
    border: 1px solid #ccc;
    background-color: #f0f0f0;
    font-weight: bold;
    text-align: left;
}
td {
    width: 33.33%;
    vertical-align: top;
    padding: 10px;
    border: 1px solid #ccc;
}
</style>
</head>
<body>
<h1>Side-by-Side Article Comparison</h1>
<table>
<tr>
<th>Original</th>
<th>First LLM summary</th>
<th>Production</th>
</tr>
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_header)

def end_side_by_side_html(filename):
    html_footer = """</table>
</body>
</html>
"""
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(html_footer)

def append_side_by_side_row(filename, article, output_picture_tags, suppress_id_in_html, replacements_for_article):
    # Left column: Always original
    left_html = "<h3>Original</h3>" + formatted_article_output(article, output_summary=False,
                                                               output_picture_tags=output_picture_tags,
                                                               suppress_id_in_html=suppress_id_in_html,
                                                               pad_margins=False, complete_html=False)
    # Middle column: Always first summary (blank if no summary required)
    if article["summarised"]:
        middle_html = "<h3>Summarised</h3>" + formatted_article_output(article, output_summary=True,
                                                                       output_picture_tags=output_picture_tags,
                                                                       suppress_id_in_html=suppress_id_in_html,
                                                                       pad_margins=False, complete_html=False)
    else:
        middle_html = ""
    # Right column: Always production
    production_article, replaced_fields, production_base_type = prepare_production_article(article,replacements_for_article)
    # Determine header for right column
    if production_base_type == 'original':
        base_label = "Original"
    elif production_base_type == 'summarised':
        base_label = "Summarised"
    elif production_base_type == 'corrected_summary':
        base_label = "Summarised with LLM corrections"
    if replaced_fields:
        right_header = f"<h3>{base_label} [with string replacements]</h3>"
    else:
        right_header = f"<h3>{base_label}</h3>"
    right_html = right_header + formatted_article_output(production_article, output_summary=False,
                                                         output_picture_tags=output_picture_tags,
                                                         suppress_id_in_html=suppress_id_in_html, pad_margins=False,
                                                         complete_html=False)
    row_html = f"""<tr>
<td>{left_html}</td>
<td>{middle_html}</td>
<td>{right_html}</td>
</tr>
"""
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(row_html)

skip_list = ["https://www.theguardian.com/music/live/2022/jun/24/glastonbury-live-2022-friday?filterKeyEvents=false&page=with:block-62b5c8e18f0875bb61abafc0",
"https://www.theguardian.com/books/2022/may/19/ruth-pen-by-emilie-pine-review-a-tale-of-two-lives" ] #These are duplicates

def print_and_flush(message):
    print(message)
    sys.stdout.flush()

def read_all_article_content(base_path):
    print_and_flush("Reading articles")
    all_json_data = {}
    subdirectories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    for subdir in subdirectories:
        print_and_flush(f"Reading articles from {subdir}")
        file_pattern = os.path.join(base_path, subdir, "*_parsed.json")
        json_files = glob.glob(file_pattern)
        for json_file in json_files:
            filename = os.path.basename(json_file)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})', filename)
            if not date_match:
                raise ValueError(f"File {filename} does not contain expected date format YYYY-MM-DD_YYYY-MM-DD")
            file_dates = f"{date_match.group(1)}_{date_match.group(2)}"
            with open(json_file, 'r', encoding='utf-8') as input_file:
                json_data = json.load(input_file)
                filtered_data = {k: v for k, v in json_data.items() if k not in skip_list}
                for article_key, article_data in filtered_data.items():
                    article_data['file_dates'] = file_dates
                all_json_data.update(filtered_data)
    print_and_flush(f"Read {len(all_json_data)} articles")
    return all_json_data

def check_and_correct_dates(articles):
    for article_key, article_data in articles.items():
        if 'date' not in article_data or article_data['date'] is None or article_data['date'] == "":
            file_dates = article_data['file_dates']
            end_date = file_dates.split('_')[1]
            article_data['date'] = end_date
            print(f"Updated missing date for article {article_key} with {end_date}")
    return articles

def select_random_articles(articles, seed=421):
    random.seed(seed)
    article_keys = [key for key in articles.keys() if not article_has_image_issues(articles[key])]
    num_to_select = min(1, len(article_keys))
    selected_keys = random.sample(article_keys, num_to_select)
    for key in articles.keys():
        if key in selected_keys:
            articles[key]['selected_for_processing'] = True
        else:
            articles[key]['selected_for_processing'] = False

def select_articles_weighted_random(articles, stop_after, seed=420):
    random.seed(seed)
    source_weights = {}
    try:
        with open("../sourceWeights.tsv", 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    source, weight = parts
                    source_weights[source] = float(weight)
    except FileNotFoundError:
        warnings.warn("sourceWeights.tsv not found, using equal weights", UserWarning)
        # Default to equal weights if file not found
        sources = set(article["source"] for article in articles.values())
        for source in sources:
            source_weights[source] = 1.0 / len(sources)
    # Group articles by source
    articles_by_source = {}
    for article in articles.values():
        source = article.get("source", "Unknown")
        if source not in articles_by_source:
            articles_by_source[source] = []
        articles_by_source[source].append(article)
    # Calculate how many articles to select from each source
    selections_by_source = {}
    for source, weight in source_weights.items():
        selections_by_source[source] = int(round(stop_after * weight))
    # Select articles randomly from each source
    selected_articles = []
    for source, count in selections_by_source.items():
        source_articles = articles_by_source.get(source, [])
        # Debug info - add before the random.sample line
        print(f"Source: {source}, Count to select: {count}, Available articles: {len(source_articles)}")
        if count > 0:  # Only process sources that need articles
            selected_articles.extend(random.sample(source_articles, count))
    for article in articles.values():
        article['selected_for_processing'] = article in selected_articles
    return selected_articles

def output_coding_headers(file_name, do_screening, do_coding):
    base_headers = ["ID", "Title", "URL", "Version", "Word count"]
    screening_headers = ([*pas.screening_code_names, "OWE_FOCUSSED", "OWE_SPECIFIC_LLM", "OWE_SPECIFIC_HUMAN", "PASSES_SCREENING", "PASSES_SCREENING_SPECIFIC", "SUMMARY_CHECK", "CORRECTION_INSTRUCTIONS", "REPLACED_FIELDS"] if do_screening else [])
    coding_headers = (pas.rating_code_names if do_coding else [])
    with open(file_name, 'w') as f:
        f.write("\t".join([*base_headers, *screening_headers, *coding_headers]) + "\n")

def output_codes(file_name, article, do_coding, do_screening, do_summarising):
    replaced_fields_str = ','.join(article.get('replaced_fields', [])) if article.get('replaced_fields') else ''

    values = [article["id"], article["title"], article["url"], "original", str(article["text_word_count"])]
    if do_screening:
        values += [str(article["screening_codes"][code_name]) for code_name in pas.screening_code_names] + [
            article["owe_focussed_llm"],
            article["owe_specific_llm"],
            article["owe_specific_human"],
            article["passes_screening"],
            article["passes_screening_specific"],
            article.get("summary_check", "no_check"),
            article.get("correction_instructions", ""),
            replaced_fields_str
        ]
    with open(file_name, 'a') as coding_output_file:
        coding_output_file.write("\t".join(values))
        if do_coding and article["passes_screening"] == "Yes":
            coding_output_file.write(
                "\t" + "\t".join(str(article["codes_text"][code_name]) for code_name in pas.rating_code_names) + "\n")
            if do_summarising and article["summarised"]:
                coding_output_file.write("\t".join([article["id"], article["title"], article["url"], "summarised", str(article["summary_word_count"])]) + "\t" * 13)
                coding_output_file.write("\t" + "\t".join(
                    str(article["codes_summary"][code_name]) for code_name in pas.rating_code_names) + "\n")
                coding_output_file.write("\t".join([article["id"], article["title"], article["url"], "legacy_resummarised", str(article["legacy_resummary_word_count"])]) + "\t" * 13)
                coding_output_file.write("\t" + "\t".join(
                    str(article["codes_legacy_resummary"][code_name]) for code_name in pas.rating_code_names) + "\n")
        else:
            coding_output_file.write("\n")
        coding_output_file.flush()  # So if something makes it fall over, at least we saved what we got

def output_summary_process(article):
    summary_process_output = produce_output_summary_process_html(article)
    summary_process_output_filename = "output_folders/summarising_HTML_output/" + sanitise_name(article["id"]) + '.html'
    with open(summary_process_output_filename, 'w', encoding='utf-8') as f:
        f.write(summary_process_output)

def output_article(filename, article, output_article_full, output_article_summarised, output_picture_tags,
                   output_individually=False, suppress_id_in_html=False, legacy_compilation=True,
                   compilation_format="none", compilation_inclusion_criterion=None, compilation_filename=None,
                   individual_output_base_path="output_folders/individual_article_output",
                   replacements_for_article=None):
    if replacements_for_article is None:
        replacements_for_article = []
    subdir = None
    base_dir = None
    if output_individually:
        if article.get("passes_screening_specific") == "Yes":
            subdir = "owe_specific"
        elif article.get("passes_screening") == "Yes":
            subdir = "owe_general"
        if subdir is not None:
            base_dir = os.path.join(individual_output_base_path, subdir)
            os.makedirs(os.path.join(base_dir, "original"), exist_ok=True)
            os.makedirs(os.path.join(base_dir, "llm_summarised"), exist_ok=True)
            os.makedirs(os.path.join(base_dir, "llm_corrected"), exist_ok=True)
            os.makedirs(os.path.join(base_dir, "production"), exist_ok=True)
    if output_article_full:
        formatted_output = formatted_article_output(article, False, output_picture_tags, suppress_id_in_html, pad_margins=True, complete_html=True)
        if output_individually and subdir is not None:
            individual_filename = os.path.join(base_dir, "original", f"{sanitise_name(article['id'])}.html")
            with open(individual_filename, 'w', encoding='utf-8') as f:
                f.write(formatted_output)
        if legacy_compilation:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(formatted_output)
    if output_article_summarised:
        if article["summarised"]:
            html_content = formatted_article_output(article, True, output_picture_tags, suppress_id_in_html, pad_margins=True, complete_html=True)
            if output_individually and subdir is not None:
                individual_filename = os.path.join(base_dir, "llm_summarised", f"{sanitise_name(article['id'])}.html")
                with open(individual_filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
        else:
            html_content = formatted_article_output(article, False, output_picture_tags, suppress_id_in_html, pad_margins=True, complete_html=True)
        if legacy_compilation:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(html_content)
    if output_individually and subdir is not None:
        if article.get("has_corrected_summary"):
            corrected_content = formatted_article_output(article, output_corrected_summary=True, output_picture_tags=output_picture_tags, suppress_id_in_html=False, pad_margins=True, complete_html=True)
            individual_filename = os.path.join(base_dir, "llm_corrected", f"{sanitise_name(article['id'])}.html")
            with open(individual_filename, 'w', encoding='utf-8') as f:
                f.write(corrected_content)
    if output_individually and subdir is not None:
        production_article, replaced_fields, production_base_type = prepare_production_article(article,replacements_for_article)
        production_content = formatted_article_output(production_article, False, output_picture_tags,suppress_id_in_html=True, pad_margins=False, complete_html=True)
        individual_filename = os.path.join(base_dir, "production", f"{sanitise_name(article['id'])}.html")
        with open(individual_filename, 'w', encoding='utf-8') as f:
            f.write(production_content)
        article['replaced_fields'] = replaced_fields
        article['production_base_type'] = production_base_type
    else:
        # Still need to prepare production article for side-by-side even if not outputting individually
        if compilation_format == "side-by-side" and compilation_inclusion_criterion is not None:
            production_article, replaced_fields, production_base_type = prepare_production_article(article,replacements_for_article)
            article['replaced_fields'] = replaced_fields
            article['production_base_type'] = production_base_type
    if compilation_inclusion_criterion is not None:
        if article[compilation_inclusion_criterion] == "Yes":
            if compilation_format == "side-by-side" and compilation_filename is not None:
                append_side_by_side_row(compilation_filename, article, output_picture_tags, suppress_id_in_html,replacements_for_article)

def prepare_production_article(article, replacements_for_article):
    # The 'text' field always contains the production text regardless of source.
    production_article = {
        'id': article['id'],
        'source': article['source'],
        'title': article['title'],
        'subtitle': article['subtitle'],
        'image': copy.deepcopy(article['image']),
        'scraped_image_missing': article.get('scraped_image_missing', False)
    }
    if article.get('has_corrected_summary'):
        production_article['text'] = article['corrected_summary']
        production_base_type = 'corrected_summary'
    elif article['summarised']:
        production_article['text'] = article['summary']
        production_base_type = 'summarised'
    else:
        production_article['text'] = article['text']
        production_base_type = 'original'
    replaced_fields = []
    for replacement in replacements_for_article:
        field = replacement['replacement_field']
        old = replacement['replaced_string']
        old = old.encode().decode('unicode_escape')
        new = replacement['replacement_string']
        new = new.replace('[DELETE]', '')
        is_fill_blank = (old == '[FILL_BLANK]')
        if field.startswith('caption'):
            caption_index = int(field[7:])  # Extract number from 'caption0', 'caption1', etc.
            if not production_article['image']:
                print(f"ERROR: Article {article['id']} has replacement for {field} but has no images")
                sys.exit(1)
            if caption_index >= len(production_article['image']):
                print(
                    f"ERROR: Article {article['id']} has replacement for {field} but only has {len(production_article['image'])} images")
                sys.exit(1)
            caption_text = production_article['image'][caption_index].get('caption', '')
            if is_fill_blank:
                if caption_text:  # Non-empty field
                    print(
                        f"ERROR: Article {article['id']} [FILL_BLANK] in {field}: field is not empty (contains '{caption_text}')")
                    sys.exit(1)
                # Empty field - populate with replacement text
                production_article['image'][caption_index]['caption'] = new
            else:
                if old not in caption_text:
                    print(
                        f"ERROR: Article {article['id']} replacement in {field}: replaced_string '{old}' not found in caption {repr(caption_text)}")
                    sys.exit(1)
                production_article['image'][caption_index]['caption'] = caption_text.replace(old, new)
            replaced_fields.append(field)
        else:
            if field not in production_article:
                print(f"ERROR: Article {article['id']} has replacement for field '{field}' which doesn't exist")
                sys.exit(1)
            field_text = production_article[field]
            if field_text is None:
                field_text = ''
            if is_fill_blank:
                if field_text:  # Non-empty field
                    print(
                        f"ERROR: Article {article['id']} [FILL_BLANK] in {field}: field is not empty (contains '{field_text}')")
                    sys.exit(1)
                production_article[field] = new
            else:
                if old not in field_text:
                    print(f"Replacing in: {repr(field_text)}")
                    print(f"ERROR: Article {article['id']} replacement in {field}: replaced_string '{old}' not found")
                    sys.exit(1)
                production_article[field] = field_text.replace(old, new)
            replaced_fields.append(field)
    return production_article, replaced_fields, production_base_type

def output_word_counts(article):
    filename = f"output_folders/article_word_count_output/counts_{timestamp}.tsv"
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"{article['id']}\t{article['source']}\t{article['title_word_count']}\t{article['subtitle_word_count']}\t{article['text_word_count']}\n")

def assemble_exclusion_list(exclusion_list):
    matches = []
    for filename in exclusion_list:
        with open(filename, 'r', encoding='utf-8') as file:
            matches.extend(line.strip() for line in file if line.strip())
    id_list = [*[sanitise_name(x) for x in matches], "Mirror_2021-10-13_Who-are-Insulate"]
    return id_list

def select_articles_from_file(articles, file_name):
    for key in articles:
        articles[key]['selected_for_processing'] = False
    with open(file_name, 'r') as f:
        for line in f:
            id_code = sanitise_name(line.strip())
            for key in articles:
                if articles[key]['id'] == id_code:
                    articles[key]['selected_for_processing'] = True
                    print("selected: " + id_code)


def filter_articles_by_date(articles, date_range_type="embargo"):
    if date_range_type == "all":
        print(f"No date filtering applied - keeping all {len(articles)} articles")
        return articles
    current_date = datetime.datetime.now()
    filtered_articles = {}
    removed_count = 0
    if date_range_type == "embargo":
        cutoff_date = current_date - datetime.timedelta(days=365 * 2)
        for url, article in articles.items():
            if "date" in article:
                try:
                    pub_date = datetime.datetime.fromisoformat(article["date"])
                    if pub_date < cutoff_date:
                        filtered_articles[url] = article
                    else:
                        removed_count += 1
                except (ValueError, TypeError):
                    warnings.warn(
                        f"Can't find a date in article at {url} that matches expected format, so possible embargo violation.",
                        UserWarning)
                    filtered_articles[url] = article
            else:
                filtered_articles[url] = article
        print(f"Embargo removed {removed_count} articles published within the last 2 years")
    elif date_range_type == "final":
        start_date = datetime.datetime.fromisoformat("2023-10-08")
        end_date = datetime.datetime.fromisoformat("2025-10-07")
        for url, article in articles.items():
            if "date" in article:
                try:
                    pub_date = datetime.datetime.fromisoformat(article["date"])
                    if start_date <= pub_date <= end_date:
                        filtered_articles[url] = article
                    else:
                        removed_count += 1
                except (ValueError, TypeError):
                    warnings.warn(f"Can't parse date for article at {url}, excluding from final dataset.", UserWarning)
                    removed_count += 1
            else:
                warnings.warn(f"Article at {url} has no date, excluding from final dataset.", UserWarning)
                removed_count += 1
        print(f"Date filtering (final) removed {removed_count} articles outside range 2023-10-08 to 2025-10-07")
    else:
        raise ValueError(f"Invalid date_range_type: {date_range_type}. Must be 'embargo', 'all', or 'final'.")
    return filtered_articles

def check_quotas_met(quota_tracker, source_quotas):
    for source, target in source_quotas.items():
        if quota_tracker.get(source, 0) < target:
            return False
    return True

def load_human_coding_for_article(article_id, database_file):
    if os.path.exists(database_file):
        with open(database_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 2 and parts[0] == article_id:
                    return parts[1]
    return None

def display_article_for_human_coding(article, output_picture_tags=False, suppress_id_in_html=False):
    output_dir = "output_folders/coding_review"
    os.makedirs(output_dir, exist_ok=True)
    html_content = formatted_article_output(article, output_summary=False, output_picture_tags=output_picture_tags, suppress_id_in_html=suppress_id_in_html, pad_margins=True, complete_html=True)
    filename = f"{sanitise_name(article['id'])}.html"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    full_path = os.path.abspath(filepath)
    subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--new-window", f"file:///{full_path}"])
    return filepath

def human_code_article(article, database_file):
    if article["passes_screening"] != "Yes":
        return None
    article_id = article["id"]
    existing_codes = {}
    if os.path.exists(database_file):
        with open(database_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    existing_codes[parts[0]] = parts[1]
    if article_id in existing_codes:
        return existing_codes[article_id]
    key_mappings = {
        'n': "Not even owe",
        'f': "Owe but fails other criteria",
        'u': "Owe unspecific",
        'g': "Owe grey-area specific",
        's': "Owe specific"
    }
    display_article_for_human_coding(article)
    print(f"\nArticle coding needed - please press a key (N/F/U/G/S)")
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key in key_mappings:
                code_value = key_mappings[key]
                print(f"Coded as: {code_value}")
                with open(database_file, 'a', encoding='utf-8') as f:
                    f.write(f"{article_id}\t{code_value}\n")
                return code_value
        time.sleep(0.1)

def check_human_code_display(article, database_file):
    article_id = article["id"]
    existing_code = load_human_coding_for_article(article_id, database_file)
    if existing_code is None:
        print(f"\nERROR: No human coding found in database for article {article_id}")
        print("This article requires human coding but none exists in the database.")
        sys.exit(1)
    display_article_for_human_coding(article)
    print(f"\nArticle {article_id}")
    print(f"Existing human coding: {existing_code}")
    print("Press any key to continue...")
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            return existing_code
        time.sleep(0.1)

def handle_owe_specific_coding( article, human_coding, check_human_coding, database_file ):
    human_code = load_human_coding_for_article(article["id"], database_file)
    if human_code is None:
        if check_human_coding != "no":
            print(f"\nERROR: No human coding found in database for article {article['id']}")
            print("This article requires human coding but none exists in the database.")
            sys.exit(1)
        elif human_coding:
            human_code = human_code_article(article, database_file)
    article["owe_specific_human"] = human_code if human_code is not None else ""
    if article["owe_specific_human"] == "Owe specific":
        article["passes_screening_specific"] = "Yes"
    else:
        article["passes_screening_specific"] = "No"
    if check_human_coding == "all" or ( check_human_coding == "passes" and article["passes_screening_specific"] == "Yes" ):
        display_article_for_human_coding(article)
        check_human_code_display(article, database_file)

def load_correction_instructions(corrections_file, articles):
    llm_corrections = {}
    replacement_corrections = {}
    if not os.path.exists(corrections_file):
        return llm_corrections, replacement_corrections
    with open(corrections_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        expected_headers = ['article_id', 'correction_type', 'correction_note', 'llm_corrections',
                            'replacement_field', 'replaced_string', 'replacement_string']
        if reader.fieldnames is None:
            print(f"ERROR: Corrections file {corrections_file} is empty or has no header")
            sys.exit(1)
        if len(reader.fieldnames) != len(expected_headers):
            print(
                f"ERROR: Corrections file header has {len(reader.fieldnames)} columns, expected {len(expected_headers)}")
            sys.exit(1)
        for i, (actual, expected) in enumerate(zip(reader.fieldnames, expected_headers)):
            if actual != expected:
                print(f"ERROR: Column {i + 1} header is '{actual}', expected '{expected}'")
                sys.exit(1)
        articles_with_llm = set()
        for line_num, row in enumerate(reader, start=2):
            article_id = row['article_id']
            correction_type = row['correction_type']
            llm_corrections_field = row['llm_corrections']
            replacement_field = row['replacement_field']
            replaced_string = row['replaced_string']
            replacement_string = row['replacement_string']
            if correction_type not in ['llm', 'replacement']:
                print(
                    f"ERROR: Line {line_num} has invalid correction_type '{correction_type}', must be 'llm' or 'replacement'")
                sys.exit(1)
            article_found = False
            for article in articles.values():
                if article["id"] == article_id:
                    article_found = True
                    break
            if not article_found:
                print(f"ERROR: Article {article_id} in corrections file not found in dataset")
                sys.exit(1)
            if correction_type == 'llm':
                if article_id in articles_with_llm:
                    print(f"ERROR: Multiple rows with correction_type 'llm' for article {article_id}")
                    sys.exit(1)
                articles_with_llm.add(article_id)
                if not llm_corrections_field:
                    print(f"ERROR: Line {line_num} has correction_type 'llm' but empty llm_corrections field")
                    sys.exit(1)
                llm_corrections[article_id] = llm_corrections_field
            elif correction_type == 'replacement':
                valid_fields = ['title', 'subtitle', 'text', 'caption0', 'caption1', 'caption2']
                if replacement_field not in valid_fields:
                    print(
                        f"ERROR: Line {line_num} has invalid replacement_field '{replacement_field}', must be one of {valid_fields}")
                    sys.exit(1)
                if not replaced_string:
                    print(f"ERROR: Line {line_num} has correction_type 'replacement' but empty replaced_string")
                    sys.exit(1)
                if article_id not in replacement_corrections:
                    replacement_corrections[article_id] = []
                replacement_corrections[article_id].append({
                    'replacement_field': replacement_field,
                    'replaced_string': replaced_string,
                    'replacement_string': replacement_string
                })
    return llm_corrections, replacement_corrections

def process_articles(
        key,
        debug_screening_process=False,
        config_file="none",
        articles_path="../article_contents",
        do_screening=False,
        do_coding=False,
        do_summarising=False,
        check_summary=False,
        very_short_summary=False,
        do_summary_corrections=False,
        corrections_instructions_file="summary_corrections.tsv",
        process_only_selected=False,
        stop_after=50,
        count_type="any",
        article_order_random_seed=420,
        output_article_full=False,
        output_article_summarised=False,
        output_article_summary_process=False,
        output_articles_individually=False,
        compilation_format="none",
        compilation_output_filename="unset",
        compilation_inclusion_criterion="passes_screening_specific",
        individual_output_base_path="output_folders/individual_article_output",
        human_coding_database_file="finalBatch7HumanCoding.tsv",
        output_detailed_word_counts=False,
        article_selection="random",
        article_exclusion_list="none",
        output_picture_tags=False,
        suppress_id_in_html=False,
        coding_output_filename="unset",
        html_output_filename="unset",
        get_owe_focussed_llm_coding=False,
        use_owe_focussed=True,
        use_owe_specific=False,
        date_range_type="embargo",
        source_quotas=None,
        quota_pad=0,
        human_coding=False,
        check_human_coding="no",
):
    if config_file != "none":
        warnings.warn("Parameter selection via configuration file is deprecated and unlikely to work appropriately.", UserWarning)
        articles_path, do_screening, do_coding, do_summarising, process_only_selected, stop_after, count_type, article_order_random_seed, output_article_full, output_article_summarised, output_article_summary_process, output_only_articles_passing_screening, output_detailed_word_counts, article_selection, article_exclusion_list, output_picture_tags, coding_output_filename, html_output_filename = load_config(
            config_file)
    if coding_output_filename == "unset":
        coding_output_filename = f"coding_output_{timestamp}.tsv"
    if html_output_filename == "unset":
        html_output_filename = f"html_output_{timestamp}.tsv"
        # Validate compilation_format parameters
    if compilation_format == "side-by-side":
        if not (output_article_full and output_article_summarised):
            print(
                "ERROR: compilation_format='Side-by-side' requires both output_article_full=True and output_article_summarised=True")
            sys.exit(1)
        if compilation_output_filename == "unset":
            compilation_output_filename = f"side_by_side_output_{timestamp}.html"
        start_side_by_side_html(compilation_output_filename)
    if debug_screening_process:
        global debug_log
        debug_log = True
        llm.no_cache = True
    else:
        llm.no_cache = False
    llm.load_client(key)
    articles = read_all_article_content(articles_path)
    articles = sanitise_ids(articles)  # dealing with poorly formed ID codes
    articles = check_and_correct_dates(articles)
    prepare_articles(articles)  # tidying, e.g. dealing with missing ID codes
    if article_exclusion_list != "none":
        exclusion_list = assemble_exclusion_list(article_exclusion_list)
        # Remove excluded articles from the dictionary
        articles = {url: article for url, article in articles.items()
                    if article["id"] not in exclusion_list}
    articles = filter_articles_by_date(articles, date_range_type)
    llm_correction_instructions_dict = {}
    replacement_corrections_dict = {}
    if do_summary_corrections:
        llm_correction_instructions_dict, replacement_corrections_dict = load_correction_instructions(corrections_instructions_file, articles)
    ids_included_in_batch = []
    if do_screening or do_coding:
        output_coding_headers(coding_output_filename, do_screening, do_coding)
    if article_selection == "random":
        random.seed(article_order_random_seed)
        articles_to_loop = random.sample(list(articles.values()), len(articles))
    elif article_selection == "random_weighted":
        articles_to_loop = select_articles_weighted_random(articles, stop_after, article_order_random_seed)
    else:
        select_articles_from_file(articles, article_selection)
        articles_to_loop = list(articles.values())
        if not process_only_selected:
            sys.exit(
                "It doesn't make sense to specify an article selection with article_selection but also allow process_only_selected to be False.")
    number_completed = 0
    quota_tracker = {} if source_quotas is not None else None
    print(f"Now processing {len(articles_to_loop)} articles")
    if quota_pad > 0 and source_quotas is not None:
        adjusted_quotas = {source: math.ceil(count * (1 + quota_pad)) for source, count in source_quotas.items()}
        print(f"Original quotas: {source_quotas}")
        print(f"Adjusted quotas: {adjusted_quotas}")
        source_quotas = adjusted_quotas
    for article in articles_to_loop:
        sys.stdout.flush()
        if quota_tracker is not None and check_quotas_met(quota_tracker, source_quotas):
            print("All source quotas met!")
            break
        if process_only_selected and not article["selected_for_processing"]: continue
        if quota_tracker is not None:  # Skip if this source has already met its quota
            source = article.get("source", "Unknown")
            source_target = source_quotas.get(source, 0)
            source_current = quota_tracker.get(source, 0)
            if source_current >= source_target:
                continue
        processing_successful = screen_and_code_article(article, do_screening, do_coding, use_owe_focussed, use_owe_specific, get_owe_focussed_llm_coding )
        if processing_successful:
            ids_included_in_batch.append(article["id"])
            if output_detailed_word_counts: output_word_counts(article)
            if do_screening and use_owe_specific:
                if article["passes_screening"] == "Yes":
                    handle_owe_specific_coding( article, human_coding, check_human_coding, human_coding_database_file )
                else:
                    article["owe_specific_human"] = "Unused"
                    article["passes_screening_specific"] = "No"
                if do_summarising and article["passes_screening_specific"] == "Yes":
                    do_summarisation_for_article(article, do_coding, very_short_summary, check_summary, do_summary_corrections, llm_correction_instructions_dict)
            elif do_summarising:
                if not do_screening or article["passes_screening"] == "Yes":
                    do_summarisation_for_article(article, do_coding, very_short_summary, check_summary, do_summary_corrections, llm_correction_instructions_dict)
            if output_article_full or output_article_summarised:
                replacements_for_article = replacement_corrections_dict.get(article["id"], [])
                output_article(html_output_filename, article, output_article_full, output_article_summarised, output_picture_tags, output_articles_individually, suppress_id_in_html, legacy_compilation=False, compilation_format=compilation_format, compilation_filename=compilation_output_filename if compilation_format == "side-by-side" else None, compilation_inclusion_criterion=compilation_inclusion_criterion, individual_output_base_path=individual_output_base_path, replacements_for_article=replacements_for_article)
            if quota_tracker is not None and do_screening and use_owe_specific:
                if article["passes_screening_specific"] == "Yes":
                    source = article.get("source", "Unknown")
                    quota_tracker[source] = quota_tracker.get(source, 0) + 1
                    all_sources = sorted(set(quota_tracker.keys()) | set(source_quotas.keys()))
                    total_tracker = sum(quota_tracker.values())
                    total_required = sum(source_quotas.values())
                    print( f"Quotas: {', '.join(f'{s}: {quota_tracker.get(s, 0)}/{source_quotas.get(s, 0)}' for s in all_sources)}")
                    print(f"Total: {total_tracker}/{total_required}")
            if do_screening or do_coding:
                output_codes(coding_output_filename, article, do_coding, do_screening, do_summarising)
            if output_article_summary_process and do_summarising:
                output_summary_process(article)
        if count_type == "any" or (count_type == "pass_screening" and article["passes_screening"] == "Yes"):
            number_completed += 1
            if number_completed >= stop_after:
                print(f"Ending because processed {number_completed} articles.")
                break
    if compilation_format == "side-by-side":
        end_side_by_side_html(compilation_output_filename)
    if quota_tracker is not None and not check_quotas_met(quota_tracker, source_quotas):
        print("\nWARNING: Ran out of articles before meeting all quotas!")
        print("Current quota status:")
        for source, target in source_quotas.items():
            current = quota_tracker.get(source, 0)
            print(f"  {source}: {current}/{target}")
        warnings.warn("Not all source quotas were met - ran out of articles", UserWarning)

#    with open( f"output_folders/batch_ran/batch_{timestamp}.txt", 'w', encoding='utf-8') as f:
#        f.write('\n'.join(ids_included_in_batch))

#if __name__ == "__main__":
#    with open('key.txt', 'r') as file:
#        file_api_key = file.read().strip()
#    process_articles("config.json", file_api_key)

if __name__ == "__main__":
    process_articles(
        debug_screening_process=True,
        articles_path="article_contents",
        count_type="pass_screening",
        stop_after=1,
        article_selection="random",
        article_order_random_seed=427,
        do_screening=True,
        do_summarising=True,
        output_article_summarised=True,
        output_only_articles_passing_screening=False,
        coding_output_filename="batch4_llm_screening.tsv",
        html_output_filename="batch4_html_output.html",
        article_exclusion_list=["coding_batches/batch2/batch2_random_selection.txt",
                                "coding_batches/batch3/batch3_random_selection.txt"]
    )

