tag_instructions_prompt_intro = """

You are going to identify content in newspaper article content by marking the start and end of content blocks that cover specific topics. The newspaper articles are all about disruptive environmental protest, and the two types of content to be marked are content about the effects of disruptive protest, and content about the messages that the protesters are attempting to convey.

You will reproduce the article content exactly as it is provided, but you will insert tags that mark the start and end of blocks of content. At the start of a block about the effects of disruptive protest, you will insert #DS (disruption start) and at the end of such a block, you will insert #DE (disruption end). At the start of a block about protester messages, you will insert #MS (messaging start) and at the end of such a block, you will insert #ME (messaging end).

There are some tags already in the article content, which relate to pictures from the original article. #PH indicates that a picture was here. #PH will normally be followed by #CS and #CE which indicate the start and end of text that is the caption for that picture. When you are coding, use the caption to determine what is in the picture, and include it in blocks if necessary, by making sure the relevant #PH tag is inside the block. For example, a picture indicated as containing banners with messages should be inside a messaging content block. As another example, a picture showing a road block should be inside a disruption effects block.

Here are more detailed definitions:
- Disruption effects content blocks contain (a) content that is clearly directly giving information about the nature of disruption, and (b) content that can reasonably be inferred to be details of disruption, given other content that is in the article. As an example of such inference, see my comment on the first picture in the example below. Actions that are reported as being planned rather than as having happened count in the same way as if they had happened.
- Messaging content blocks contain only information about messages protesters are trying to convey. The means with which they are reported as conveying the message (e.g., banner, quote from spokesperson) is not included in the messaging block. Often messaging content blocks will simply be quotes (from a person or a banner). Sometimes they will be a reported summary of some things protesters said. Take care to include messaging only from protesters or their allies - not messaging from critics of protesters.

Use this definition of disruptive protest: Disruptive protest is protest that appears to be aimed at disrupting the functioning of some other activity generally regarded as legitimate (whether that is fossil fuel operations, road transport, sport, government operations, cultural displays, etcetera) as a means to draw attention to a cause or as a means to prevent the activity. Disruption is not dependent on the actual scale of disturbance of economic or social life. For example, a registered march in a city can cause great inconvenience, but because the disruption is a side-effect of the marchers’ primary intention to amplify their communications by gathering in numbers, we do not regard this as disruptive protest. Protest conducted by groups that often disrupt is not inherently disruptive. Such groups sometimes protest in ways that superficially resemble their disruptive protests without intending to disrupt on that occasion.

The two types of content block can potentially overlap. Here is an example I created in order to illustrate both overlap and the fact that messaging content blocks don't include the manner by which the messaging is conveyed: "Extinction Rebellion protesters were on the streets of London today. #DS They blocked a main road using a banner saying #MS 'End Fossil Fuels Now'. #ME #DE Minister Priti Patel said 'This government will never give in to the eco-yobs.'"

The articles come in sections: ID, title, subtitle, and main content (marked just as content). Do not code the ID but code the other three subsections. The Subtitle may be missing. Do not start a content block in one section and carry it over into the next section. End the block and if necessary start it again in the next section. 

Below are three articles that have already been coded in this manner. Note, there are also comments on the article that help explain the justification for coding choices made. The places in the material that the comments apply to are marked [COMMENTX] where X is a number, and the same [COMMENTX] identifiers appear at the end where the comments themselves are given.

ID: BBC_2020-09-05_Extinction-Rebellion-protesters
Source: BBC
Title: #DS Extinction Rebellion protesters block newspaper printing presses #DE[COMMENT1]
Content: #DS[COMMENT2] #PH #CS Protesters gathered outside the sites - including Broxbourne in Hertfordshire - owned by Rupert Murdoch's News Corporation #CE [COMMENT3]
Extinction Rebellion (XR) activists have delayed the distribution of several national newspapers after blocking access to three printing presses owned by Rupert Murdoch. Protesters targeted Newsprinters presses at Broxbourne in Hertfordshire, Knowsley in Merseyside, and near Motherwell, North Lanarkshire. #DE[COMMENT4] Prime Minister Boris Johnson said the action was "unacceptable".

#DS Eighty people have been arrested.[COMMENT5] The presses print the Rupert Murdoch-owned News Corp titles including the Sun, the Times, the Sun on Sunday, the Sunday Times, and the Scottish Sun. They also print the Daily Telegraph and Sunday Telegraph, the Daily Mail and Mail on Sunday, and the London Evening Standard.[COMMENT6]

XR used vehicles to block roads to the printing plants, while individual protesters chained themselves to structures. [COMMENT7]#DE[COMMENT8] Vans were covered with banners with messages including #MS "Free the truth" and "Refugees are welcome here"[COMMENT9].

Demonstrators have accused the papers of failing to report on climate change. #ME[COMMENT10] Boris Johnson said, "A free press is vital in holding the government and other powerful institutions to account on issues critical for the future of our country, including the fight against climate change. It is completely unacceptable to seek to limit the public's access to news in this way."
#DS[COMMENT11] #PH #CS XR used vehicles along with individual protesters chaining themselves to structures to block roads to the presses #CE 

Hertfordshire Police said officers were called to Great Eastern Road[COMMENT12] near the Broxbourne plant at about 22:00 BST, where they found about 100 protesters who had "secured themselves to structures and one another". By 06:00 delivery lorries had still been unable to leave the site to distribute papers. #DE[COMMENT13]

#MS XR has accused the newspapers and their owners of "failure to report on the climate and ecological emergency" and "polluting national debate" on dozens of social issues. The group is calling on the government to do more to act on climate change. #ME[COMMENT14]

ID: BBC_2020-09-20_GM-crops_-The
Source: BBC
Title: GM crops: [COMMENT15]#DS The Greenpeace activists who risked jail to destroy a field of maize #DE
Content: #DS [COMMENT16]#PH#CS Greenpeace protesters destroy a field of GM crops at Lyng, Norfolk on 26 July 1999 #CE 
In a landmark environmental protest, 28 Greenpeace activists destroyed a field of genetically-modified (GM) maize on a farm in Norfolk in July 1999. #DE[COMMENT17] The group, which included a vicar and a beauty consultant, was led by Greenpeace executive director Lord Peter Melchett, a former government minister and Norfolk farmer.

#DS[COMMENT18] At 05:00 BST on 26 July, the protesters stormed the six-acre field of modified fodder maize, trampling and pulling at the 7ft plants. They used a machine with whirling 4ft blades to destroy a large section of the crop, planning to bag it up and deliver it to Norfolk-based GM contractors AgrEvo. #DE

#MS The activists opposed such trials, claiming they would cause genetic pollution of the environment. #ME Michael Uwins, Greenpeace's East of England co-ordinator, stated, #MS "We totally believed in what we were doing. We were not anti-science or GM as such; it was about open-air field trials. It was irresponsible and had to be stopped." #ME
#PH#CS Now 74, Michael Uwins describes himself as an "armchair activist" #CE 

The protesters were confronted by the "furious" landowner William Brigham and family members, who were "ramming and chasing the protesters around the field." #DS Police soon arrived, and the activists were arrested and charged with criminal damage and theft. #DE

In court, the #MS protesters argued they had lawful excuse for their actions, aiming to prevent neighbouring land from being unlawfully invaded by genetically-modified pollen. #ME After two trials, all defendants were acquitted on 20 September 2000.

The verdict was seen as a triumph by environmental activists but described as "perverse" by the National Farmers' Union, which claimed it gave "the green light to wanton vandalism and trespass."

This key moment in environmental protest brought the issue of GM crops to the attention of politicians, regulators, and the media, resulting in a more cautious approach to GMO release in the UK.
#DS #PH#CS Lord Peter Melchett was arrested at the scene #CE #DE

ID: BBC_2020-09-01_Arrests-as-Extinction
Source: BBC
Title: #DS Arrests as Extinction Rebellion protests begin across England #DE
Content: #DS #PH#CS Extinction Rebellion said it planned to "peacefully disrupt" Parliament with 10 days of demonstrations #CE 
At least 90 people have been arrested at climate change protests causing disruption across England. Extinction Rebellion organised action in London #DE to #MS urge the government to prepare for a "climate crisis" #ME. #DS Campaigners were arrested after they sat in the middle of the road next to Parliament Square to stop traffic. #DE

#DS[COMMENT19] Extinction Rebellion said #MS[COMMENT20] it planned to "peacefully disrupt the UK Parliament in London" with 10 days of demonstrations until MPs backed the Climate and Ecological Emergency Bill. #ME Other planned events in the capital include a #MS "carnival of corruption" #ME[COMMENT21], which is due to take place outside the Treasury, and a #MS "walk of shame" #ME near the Bank of England. #DE

Protester Karen Wildin, a 56-year-old tutor from Leicester, said: #MS "I'm here today because I have serious concerns about the future of the planet - we need to put this above anything else. Never mind Covid, never mind A-levels, this is the biggest crisis facing us and we need to raise the message as loudly as possible." #ME
#DS #PH#CS The Met said the protests could result in "serious disruption" to businesses and commuters #CE #DE

Sarah Lunnon, a member of Extinction Rebellion, said: #MS "The failure to act on this issue will have a catastrophic impact on the future of us and the generations to come. We want to occupy Parliament Square to make our voices heard. Of course we're in the middle of a pandemic but we're balancing the risk, this is the biggest issue facing us." #ME

The Metropolitan Police said Tuesday's gathering could only take place off the main roads at Parliament Square Gardens between 08:00 BST and 19:00. Boats, vehicles, trailers or other structures were banned from the procession. The same rules apply for Wednesday's demonstrations.[COMMENT22]

#DS Met Commander Jane Connors said: "The reason we have implemented these conditions is that we know these protests may result in serious disruption to local businesses, commuters and our communities and residents, which I will not tolerate."

Last year, more than 1,700 arrests were made during Extinction Rebellion's 10-day Autumn Uprising.
#PH#CS Protesters gathered in Westminster to urge the government to prepare for a "climate crisis" #CE #DE

[COMMENT1]Note, the entire title is clearly about disruption, so it’s a disruption content block. The block ends even though the first content (which happens to be a picture) is also about disruption, because we don’t continue blocks across sections (title, subtitle (which is missing here), and main text (which starts “Content:”)).
[COMMENT2]Note – this #DS (disruption start) is before the #PH (picture here). This means the picture is included in the block of disruption content. I did this because I judge that the picture itself is illustrating disruption. I judge this because later in the article is says “XR used vehicles to block roads to the printing plants” so it’s beyond reasonable doubt that the picture that shows a protester on top of a vehicle surrounded by police is illustrating something disruptive.
[COMMENT3]Note – no #DE yet, so we are still in a disruption content block, because I judge the picture caption is continuing to explicitly describe disruption, because it says “Protesters gathered outside the sites” and includes further details that help us understand the target of the disruption. 
[COMMENT4]Now I ended the disruption block because while everything up to here was detailing disruption, the Johnson quote is commenting on the disruption rather than describing it.
[COMMENT5]How many are arrested gives information about the level of disruption, so we start a disruption block again.
[COMMENT6]Still in a disruption block because this is clearly information about which newspapers may have been affected by the disruption.
[COMMENT7]Still obviously about the nature of the disruption so still inside the disruption content block.
[COMMENT8]I ended the disruption block here because although the vans were used to cause disruption, the information about what they were “covered with” doesn’t tell us anything more about the disruption itself.
[COMMENT9]Clearly this is about the message – but note that the means with which it is conveyed is not included.
[COMMENT10]Note the messaging block ends here because the sentence following the banners is also reporting on the protesters’ reasons for the protest, which is definitely part of their messaging. But again, the Johnson quote is neither provided details of the disruption not the protesters messaging.
[COMMENT11]Starting a disruption block here because the picture and the caption are about the disruption, for the same way that the previous picture was.
[COMMENT12]I considered not including this in the disruption block because information about what police do is not necessarily about the details of disruption, but I left it in because the police came because of the disruption and because police being required to attend to deal with disruption is itself part of the disruption.
[COMMENT13]The next bit is only about protesters messaging so the disruption block ends here.
[COMMENT14]The entire paragraph was clearly about the protesters’ messaging.
[COMMENT15]Note, I didn’t include this first bit of the title in the disruption content block as this part of it doesn’t tell us anything about the disruption.
[COMMENT16]I justify the inclusion of the picture in the same way as in the previous article.
[COMMENT17]I ended the disruption block here because although everything till now (including picture and caption) has been detailing the disruptive acts, the details of the occupations of the protesters doesn’t tell us about the disruption they carried out.
[COMMENT18]I’m no longer commenting on choices that are by now (I hope) obvious.
[COMMENT19]Note that actions reported as planned count in the same way as is they have happened.
[COMMENT20]Note, this messaging block begins while still in a disruption block, because the threat to disrupt unless demands are met is both part of messaging and part of a description of disruption.
[COMMENT21]I judge the reporting of the name protesters gave to their own action to be reporting of the protesters messaging, as they have clearly chosen the name to send a message.
[COMMENT22]I didn’t put this in a disruption block because it’s not clear whether these conditions relate to anything that was actually planned or happened.

End of three example articles. Here is the article for you to tag:
"""

test_article = """
ID: BBC_2020-09-04_Extinction-Rebellion_-More
Source: BBC
Title: Extinction Rebellion: More than 300 arrested at London climate protests
Content: #PH  #CS Extinction Rebellion has planned 10 days of action and wants the government to declare a climate and ecological emergency #CE 
More than 300 people have been arrested during the third day of climate change protests in central London.

Extinction Rebellion, which has planned 10 days of action, and other groups gathered at city landmarks on Thursday.

Of those arrested, Scotland Yard said, more than 200 were linked to a demonstration on Lambeth Bridge near the Houses of Parliament.

Extinction Rebellion said police had refused to let peaceful protesters leave the bridge.

The bridge was blocked when some protesters "locked on" and attached themselves to it, police said.

It has since reopened to traffic.

Elsewhere, protesters from the group Animal Rebellion glued themselves to the top and the inside of slaughterhouse truck painted pink.
#PH  #CS Getty Images Protesters glued to the top of a slaughterhouse van painted pink #CE 
The vehicle was cordoned off after being parked sideways across Victoria Street.

Protesters also glued themselves to the ground around Parliament, while others staged sit-ins around the perimeter of the parliamentary estate.

Extinction Rebellion said it wants the government to declare a climate and ecological emergency, reduce greenhouse gas emissions to net zero by 2025 and establish a "citizens' assembly on climate and ecological justice".

More protests are planned on Friday and the Met has imposed restrictions on one event due to be held in Parliament Square.

It has ordered campaigners to stay off main roads and to leave the area by 19:00 BST.
"""

tag_instructions_prompt_end = """
End of article for tagging. Now respond with the entire article in its original format exactly as I provided it, except with the addition of #DS, #DE, #MS, and #ME tags, as appropriate. 
"""

have_another_go_no_error_prompt = """
Sometimes mistakes are made. The formatting of your tagging is correct - good - but sometimes the wrong content is tagged. Please check your previous output for compliance to the rules of this tagging task. If you have made any mistakes, please produce new output that corrects the mistakes. If you have not made any mistakes, please repeat the previous output.
"""

have_another_go_after_error_prompt = """
Sometimes mistakes are made. There is indeed a format error in your tagging. It's also possible the wrong content is tagged, but this has not been checked and it may be correct. Please check your previous output for compliance to the rules of this tagging task and produce new output that corrects the mistakes. The error that your tagging has raised is:
"""

#For example, it is possible that blocks started with #DS might not have been ended with #DE

import json
import llmproc_core as llm
client = llm.load_client()
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
llm_system_instruction = ""

import warnings

warning_log_filename = f"warnings_{timestamp}.log"

def custom_formatwarning(message, category, *_args, **_kwargs ):
    formatted_warning = f"{datetime.datetime.now()}: {category.__name__}: {message}\n"
    with open(warning_log_filename, 'a') as log_file:
        log_file.write(formatted_warning)
    return formatted_warning

warnings.formatwarning = custom_formatwarning

def llm_tag_first_go(article):
    article_string = reconstitute_article_string(article)
    id_line = article_string.splitlines()[0]
    prompt = tag_instructions_prompt_intro + article_string + tag_instructions_prompt_end
    return llm.send_prompt(prompt, client, llm_system_instruction, id_line)

def llm_tag_second_go_after_error(article):
    return llm_tag_second_go( article, have_another_go_after_error_prompt + article["tag_error_message"] )

def llm_tag_second_go_no_error(article):
    return llm_tag_second_go( article, have_another_go_no_error_prompt )

def llm_tag_second_go(article,have_another_go_prompt):
    article_string = reconstitute_article_string(article)
    id_line = article_string.splitlines()[0]
    original_prompt = tag_instructions_prompt_intro + article_string + tag_instructions_prompt_end
    return llm.send_prompt(have_another_go_prompt, client, llm_system_instruction, id_line, original_prompt, article["tag_first_go"])

def reconstitute_article_string(article):
    return_string = f"ID: {article['id']}\nSource: {article['source']}\nTitle: {article['title']}\n"
    if article.get("subtitle"):
        return_string += f"Subtitle: {article['subtitle']}\n"
    return return_string + f"Content: {article['main_content']}"

def parse_article_from_tag_string(content):
    return list(parse_articles_string(content).values())[0]

def parse_articles_string(content):
    coded_articles = {}
    current_article = {}
    content_lines = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('ID:'):
            if current_article:
                if content_lines:
                    current_article['main_content'] = '\n'.join(content_lines)
                article_id = current_article['id']
                coded_articles[article_id] = current_article.copy()
            current_article = {}
            content_lines = []
            current_article['id'] = line[3:].strip()
        elif line.startswith('Source:'):
            current_article['source'] = line[7:].strip()
        elif line.startswith('Title:'):
            current_article['title'] = line[6:].strip()
        elif line.startswith('Subtitle:'):
            current_article['subtitle'] = line[9:].strip()
        elif line.startswith('Content:'):
            if line[8:].strip():  # If there's content on the same line
                content_lines.append(line[8:].strip())
        else:
            content_lines.append(line)
    if current_article:
        if content_lines:
            current_article['main_content'] = '\n'.join(content_lines)
        article_id = current_article['id']
        coded_articles[article_id] = current_article.copy()
    return coded_articles

def parse_articles_file(filename):
    content = open(filename, 'r', encoding='utf-8').read()
    return parse_articles_string(content)

class InvalidTagNestingError(Exception):
    """Custom exception for invalid tag nesting"""
    pass

def ensure_tags_have_spaces(content):
    for tag in ['#MS', '#ME', '#DS', '#DE', '#PH', '#CS', '#CE']:
        content = content.replace(tag, f' {tag} ')
    return content

def analyze_field_tags(content):
    stats = {
        'total_words': 0,
        'messaging_words': 0,
        'disruption_words': 0,
        'total_pictures': 0,
        'messaging_pictures': 0,
        'disruption_pictures': 0
    }
    content = ensure_tags_have_spaces(content)
    messaging_depth = 0
    disruption_depth = 0
    words = []
    current_word = ''
    for char in content:
        if char.isspace():
            if current_word:
                words.append(current_word)
                current_word = ''
        else:
            current_word += char
    if current_word:
        words.append(current_word)
    valid_tags = {'#MS', '#ME', '#DS', '#DE', '#PH', '#CS', '#CE'}
    i = 0
    while i < len(words):
        word = words[i]
        if word in valid_tags:
            if word == '#MS':
                if messaging_depth > 0:
                    raise InvalidTagNestingError("Nested messaging blocks are not allowed")
                messaging_depth += 1
            elif word == '#ME':
                if messaging_depth == 0:
                    raise InvalidTagNestingError("Found #ME without matching #MS")
                messaging_depth -= 1
            elif word == '#DS':
                if disruption_depth > 0:
                    raise InvalidTagNestingError("Nested disruption blocks are not allowed")
                disruption_depth += 1
            elif word == '#DE':
                if disruption_depth == 0:
                    raise InvalidTagNestingError("Found #DE without matching #DS")
                disruption_depth -= 1
            elif word == '#PH':
                stats['total_pictures'] += 1
                if messaging_depth > 0:
                    stats['messaging_pictures'] += 1
                if disruption_depth > 0:
                    stats['disruption_pictures'] += 1
        else:
            stats['total_words'] += 1
            if messaging_depth > 0:
                stats['messaging_words'] += 1
            if disruption_depth > 0:
                stats['disruption_words'] += 1
        i += 1
    if messaging_depth > 0:
        raise InvalidTagNestingError("Unclosed messaging block at end of content")
    if disruption_depth > 0:
        raise InvalidTagNestingError("Unclosed disruption block at end of content")
    return stats

def count_words_in_tagged_blocks(article):
    for field in ['title', 'subtitle', 'main_content']:
        if field in article and article[field]:
            try:
                article[field + '_analysis'] = analyze_field_tags(article[field])
            except InvalidTagNestingError as e:
                warnings.warn(f"Error in tags for article {article["id"]}.")
                article[field + '_analysis'] = f"Error in {field}: {str(e)}"
                article["tag_error"] = "present"

def move_tags_to_main_fields(articles, which_go):
    output_path = f"tmp_{timestamp}_{which_go}.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        for article in articles.values():
            f.write(article.get(which_go, f"ERROR: tagging {which_go} not found")+"\n")
    return parse_articles_file(output_path)

def write_word_counts_file(articles, append_file=""):
    output_path = f'output_folders/article_content_block_word_counts/block_word_counts_{timestamp}_{append_file}.tsv'
    stat_fields = [
        'total_words', 'messaging_words', 'disruption_words',
        'total_pictures', 'messaging_pictures', 'disruption_pictures'
    ]
    content_types = ['title', 'subtitle', 'main_content']
    header = ['id']
    for content_type in content_types:
        for stat in stat_fields:
            header.append(f'{content_type}_{stat}')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\t'.join(header) + '\n')
        for article_id, article in articles.items():
            row = [article_id]
            for content_type in content_types:
                analysis_key = f'{content_type}_analysis'
                analysis_dict = article.get(analysis_key, {})
                if isinstance(analysis_dict, dict):
                    for stat in stat_fields:
                        row.append(str(analysis_dict.get(stat, 0)))
                else:
                    row.extend(['0'] * len(stat_fields))
            f.write('\t'.join(row) + '\n')

def attach_tagging_error_to_original_article(article,tagged_article):
    if tagged_article.get("tag_error","") == "present":
        article["tag_error_message"] = "\n".join(
            value for value in [
                tagged_article.get("title_analysis", ""),
                tagged_article.get("subtitle_analysis", ""),
                tagged_article.get("main_content_analysis", "")
            ]
            if isinstance(value, str) and "Error" in value
        )

def count_vanessa_batch_3():
    articles_for_counting = parse_articles_file('Formatted_Articles_20241118_195911 (Vanessa_Coding_50_corrected).txt')
    #articles_for_counting = parse_articles_file('Formatted_Articles_20241118_195911 (Vanessa_Coding_30_corrected).txt')
    for article in articles_for_counting.values():
        count_words_in_tagged_blocks(article)
    with open('human_coded_content_blocks.json', 'w') as f:
        json.dump(articles_for_counting, f, indent=4)
    write_word_counts_file(articles_for_counting, "assistant")

def llm_code_and_count():
    articles_for_coding = parse_articles_file('formatted_articles_20241118_195911 (for coding).txt')
    #articles_for_coding = dict(list(articles_for_coding.items())[7:9])
    articles_with_first_tagging = {}
    articles_with_second_tagging = {}
    for article in articles_for_coding.values():
        article["tag_first_go"] = llm.process_with_cache(llm_tag_first_go, article)
        article_with_first_tagging = parse_article_from_tag_string(article["tag_first_go"])
        count_words_in_tagged_blocks(article_with_first_tagging)
        articles_with_first_tagging[article_with_first_tagging["id"]] = article_with_first_tagging
        if article_with_first_tagging.get("tag_error","") == "present":
            attach_tagging_error_to_original_article(article,article_with_first_tagging)
            article["tag_second_go"] = llm.process_with_cache(llm_tag_second_go_after_error, article)
        else:
            article["tag_second_go"] = llm.process_with_cache(llm_tag_second_go_no_error, article)
        article_with_second_tagging = parse_article_from_tag_string(article["tag_second_go"])
        count_words_in_tagged_blocks(article_with_second_tagging)
        articles_with_second_tagging[article_with_second_tagging["id"]] = article_with_second_tagging
    with open('llm_coded_content_blocks.json', 'w') as f:
        json.dump(articles_with_second_tagging, f, indent=4)
    write_word_counts_file(articles_with_first_tagging, "first")
    write_word_counts_file(articles_with_second_tagging, "second")

def main():
    #llm_code_and_count()
    count_vanessa_batch_3()

if __name__ == "__main__":
    main()

