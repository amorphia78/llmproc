tag_instructions_prompt_intro = """

You are going to identify content in newspaper articles by marking the start and end of content blocks that cover specific topics. The newspaper articles are all about disruptive environmental protest. Disruptive protest is defined as follows:

Disruptive protest is protest that appears to be aimed at disrupting the functioning of some other activity generally regarded as legitimate (whether that is fossil fuel operations, road transport, sport, government operations, cultural displays, etcetera) as a means to draw attention to a cause or as a means to prevent the activity. Disruption is not dependent on the actual scale of disturbance of economic or social life. For example, a registered march in a city can cause great inconvenience, but because the disruption is a side-effect of the marchers’ primary intention to amplify their communications by gathering in numbers, we do not regard this as disruptive protest. Protest conducted by groups that often disrupt is not inherently disruptive. Such groups sometimes protest in ways that superficially resemble their disruptive protests without intending to disrupt on that occasion.

These are the five types of content to be marked. Note, actions that are reported as being planned rather than as having happened count in the same way as if they had happened.

DISRUPTION effects (direct or knock-on) of the disruptive protest. If article content superficially seems like it describes a disruption effect, then it does - there are no special reasons why some descriptions of disruption effects don't count. Knock-on effects such as court proceedings do count as disruption effects. Start tag: #DS. End tag: #DE.
PROTESTER MESSAGING - the messages protesters are trying to convey, for example quotes (from a person or on a banner) or reported summaries of things protesters said. Take care to include messaging only from protesters or their allies, not messaging from critics of protesters. Start tag: #MS. End tag: #ME.
POSITIVE COMMENTS - approval of the protest, protesters, or the protest's effects (and only those), expressed by anyone except the protesters themselves. This might be expressed by any quoted individual in any capacity in any way (e.g., politician, commentator, but not the protesters), or reported in general terms (e.g., “passers-by shouted approvingly”), or expressed by the author of the article. Start tag: #PS. End tag: #PE.
NEGATIVE COMMENTS - criticism of the protest, protesters, or the protest's effects (and only those), expressed by any quoted individual in any capacity in any way (e.g. a judge when sentencing, police, politician, commentator, other environmentalist, member of the public), reported in general terms (e.g., “passers-by shouted disapprovingly”), or expressed by the author of the article. Start tag: #NS. End tag: #NE.

You will mark content blocks by inserting start and end tags into the article text. You will reproduce the article content exactly as it is provided, but you will insert tags that mark the start and end of blocks of content. All content that is of a type defined above must be marked as being inside a content block of the correct type.  Different types of content block can potentially overlap, because content could fulfil criteria to be included in more than one category. Here is an example created to illustrate this: "Extinction Rebellion protesters were on the streets of London today. #DS They blocked a main road using #MS a banner saying 'End Fossil Fuels Now'. #ME #DE #NS Minister Priti Patel said 'This government will never give in to the eco-yobs.' #NE"

The articles come in sections: ID, title, subtitle, and main content (marked just as content). Do not code the ID but code the other three sections. The Subtitle may be missing. Do not start a content block in one section and carry it over into the next section. End the block and if necessary start it again in the next section. 

There are some tags already in the article content, relating to pictures from the original article. #PH indicates that a picture was here. #PH will normally be followed by #CS and #CE which indicate the start and end of text that is the caption and alt text for that picture. When you are coding, use the caption and alt text to determine what is in the picture, and include it in blocks if necessary, by making sure the relevant #PH tag is inside the block. For example, a picture indicated as containing banners with messages should be inside a messaging content block. As another example, a picture showing a road block should be inside a disruption effects block.

Below are four articles that have already been coded in this manner. Note, there are also comments on the article that help explain the justification for coding choices made. The places in the material that the comments apply to are marked [COMMENTX] where X is a number, and the same [COMMENTX] identifiers appear at the end where the comments themselves are given.


ID: BBC_2020-09-05_Extinction-Rebellion-protesters
Source: BBC
Title: #DS Extinction Rebellion protesters block newspaper printing presses #DE[COMMENT1]
Content: #DS[COMMENT2] #PH #CS Protesters gathered outside the sites - including Broxbourne in Hertfordshire - owned by Rupert Murdoch's News Corporation (Alt: Protesters climbing on a vehicle at a blockade near the Broxbourne printing press)#CE [COMMENT3]
Extinction Rebellion (XR) activists have delayed the distribution of several national newspapers after blocking access to three printing presses owned by Rupert Murdoch. Protesters targeted Newsprinters presses at Broxbourne in Hertfordshire, Knowsley in Merseyside, and near Motherwell, North Lanarkshire. #DE[COMMENT4] #NS Prime Minister Boris Johnson said the action was "unacceptable" #NE[COMMENT5].



#DS [COMMENT6] Eighty people have been arrested. The presses print the Rupert Murdoch-owned News Corp titles including the Sun, the Times, the Sun on Sunday, the Sunday Times, and the Scottish Sun. They also print the Daily Telegraph and Sunday Telegraph, the Daily Mail and Mail on Sunday, and the London Evening Standard.[COMMENT7]



XR used vehicles to block roads to the printing plants, while individual protesters chained themselves to structures. [COMMENT8]#DE[COMMENT9] #MS Vans were covered with banners with messages including "Free the truth" and "Refugees are welcome here".



Demonstrators have accused the papers of failing to report on climate change. #ME[COMMENT10] #NS Boris Johnson said, "A free press is vital in holding the government and other powerful institutions to account on issues critical for the future of our country, including the fight against climate change. It is completely unacceptable to seek to limit the public's access to news in this way." #NE
#DS[COMMENT11] #PH #CS XR used vehicles along with individual protesters chaining themselves to structures to block roads to the presses (Alt: Protesters climbing and chaining themselves to structures outside a printing press)#CE 


Hertfordshire Police said officers were called to Great Eastern Road[COMMENT12] near the Broxbourne plant at about 22:00 BST, where they found about 100 protesters who had "secured themselves to structures and one another". By 06:00 delivery lorries had still been unable to leave the site to distribute papers. #DE[COMMENT13]



#MS XR has accused the newspapers and their owners of "failure to report on the climate and ecological emergency" and "polluting national debate" on dozens of social issues. The group is calling on the government to do more to act on climate change. #ME[COMMENT14]


ID: BBC_2020-09-20_GM-crops_-The
Source: BBC
Title: GM crops: [COMMENT15]#DS The Greenpeace activists who risked jail to destroy a field of maize #DE
Content: #DS [COMMENT16]#PH#CS Greenpeace protesters destroy a field of GM crops at Lyng, Norfolk on 26 July 1999 (Alt: Greenpeace activists in white overalls destroying a field of maize)#CE 
In a landmark environmental protest, 28 Greenpeace activists destroyed a field of genetically-modified (GM) maize on a farm in Norfolk in July 1999. #DE[COMMENT17] The group, which included a vicar and a beauty consultant, was led by Greenpeace executive director Lord Peter Melchett, a former government minister and Norfolk farmer.



#DS[COMMENT18] At 05:00 BST on 26 July, the protesters stormed the six-acre field of modified fodder maize, trampling and pulling at the 7ft plants. They used a machine with whirling 4ft blades to destroy a large section of the crop, planning to bag it up and deliver it to Norfolk-based GM contractors AgrEvo. #DE



#MS The activists opposed such trials, claiming they would cause genetic pollution of the environment. Michael Uwins, Greenpeace's East of England co-ordinator, stated, "We totally believed in what we were doing. We were not anti-science or GM as such; it was about open-air field trials. It was irresponsible and had to be stopped." #ME[COMMENT19]
#PH#CS Now 74, Michael Uwins describes himself as an "armchair activist" (Alt: An elderly smiling man standing on a beach) #CE 


#NS The protesters were confronted by the "furious" landowner William Brigham and family members, who were "ramming and chasing the protesters around the field." #NE [COMMENT20]#DS Police soon arrived, and the activists were arrested and charged with criminal damage and theft. #DE



#MS In court, the protesters argued they had lawful excuse for their actions, aiming to prevent neighbouring land from being unlawfully invaded by genetically-modified pollen. #ME After two trials, all defendants were acquitted on 20 September 2000.



The verdict was seen as a triumph by environmental activists but #NS described as "perverse" by the National Farmers' Union, which claimed it gave "the green light to wanton vandalism and trespass." #NE[COMMENT21]



This key moment in environmental protest brought the issue of GM crops to the attention of politicians, regulators, and the media, resulting in a more cautious approach to GMO release in the UK.
#DS #PH#CS Lord Peter Melchett was arrested at the scene (Alt: An environmental protester in a field being arrested by a police officer) #CE #DE


ID: BBC_2020-09-01_Arrests-as-Extinction
Source: BBC
Title: #DS Arrests as Extinction Rebellion protests begin across England #DE
Content: #DS #PH#CS Extinction Rebellion said it planned to "peacefully disrupt" Parliament with 10 days of demonstrations (Alt: An activist from the climate protest group Extinction Rebellion is carried away by police officers) #CE 
At least 90 people have been arrested at climate change protests causing disruption across England. Extinction Rebellion organised action in London to #MS urge the government to prepare for a "climate crisis" #ME. Campaigners were arrested after they sat in the middle of the road next to Parliament Square to stop traffic. #DE



#DS[COMMENT22] #MS[COMMENT23] Extinction Rebellion said it planned to "peacefully disrupt the UK Parliament in London" with 10 days of demonstrations until MPs backed the Climate and Ecological Emergency Bill. #ME Other planned events in the capital include a #MS "carnival of corruption", which is due to take place outside the Treasury, and a "walk of shame" near the Bank of England. #ME #DE



#MS Protester Karen Wildin, a 56-year-old tutor from Leicester, said: "I'm here today because I have serious concerns about the future of the planet - we need to put this above anything else. Never mind Covid, never mind A-levels, this is the biggest crisis facing us and we need to raise the message as loudly as possible." #ME
#DS #PH#CS The Met said the protests could result in "serious disruption" to businesses and commuters (Alt: An activist lying in the street is spoken to by police officers) #CE #DE


#MS Sarah Lunnon, a member of Extinction Rebellion, said: "The failure to act on this issue will have a catastrophic impact on the future of us and the generations to come. We want to occupy Parliament Square to make our voices heard. Of course we're in the middle of a pandemic but we're balancing the risk, this is the biggest issue facing us." #ME


#PS Professor Peter Franklin, who studies climate change at a London University, said: "Although not everyone welcomes the protests, I see them as necessary to help bring about more action on climate change." #PE


The Metropolitan Police said Tuesday's gathering could only take place off the main roads at Parliament Square Gardens between 08:00 BST and 19:00. Boats, vehicles, trailers or other structures were banned from the procession. The same rules apply for Wednesday's demonstrations.[COMMENT24]



#DS #NS Met Commander Jane Connors said: "The reason we have implemented these conditions is that we know these protests may result in serious disruption to local businesses, commuters and our communities and residents, which I will not tolerate." #NE



Last year, more than 1,700 arrests were made during Extinction Rebellion's 10-day Autumn Uprising.
#PH#CS Protesters gathered in Westminster to urge the government to prepare for a "climate crisis" (Alt: A line of police surrounds a crowd of protesters) #CE #DE

ID: sun_example
Source: Sun
Title: #DS #NS Eco-zealots glue themselves #NE to priceless painting #DE
Subtitle: #DS Gallery chaos as protesters strike again #DE
Content: #DS #NS Eco-zealots brought a top London gallery to a standstill #NE yesterday after supergluing themselves to a masterpiece worth millions.
#NS The barmy activists caused mayhem #NE at the National Gallery when they attached their hands to the frame of a Van Gogh painting during the morning rush.
#NS Furious visitors were left fuming #NE as security guards scrambled to deal with the protesters, #MS who were chanting slogans about climate change. #ME #DE

[COMMENT1]Note, the entire title is clearly about disruption, so it’s a disruption content block. The block ends even though the first content (which happens to be a picture) is also about disruption, because we don’t continue blocks across sections (title, subtitle (which is missing here), and main text (which starts “Content:”)).
[COMMENT2]Note – this #DS (disruption start) is before the #PH (picture here). This means the picture is included in the block of disruption content - appropriate because the caption and the alt text indicate that the picture illustrates disruption.
[COMMENT3]Note – no #DE yet, so we are still in a disruption content block, because the article text following the picture describes disruption. 
[COMMENT4]Now I ended the disruption block because while everything up to here was detailing disruption, the Johnson quote is commenting on the disruption rather than describing it.
[COMMENT5]This is clearly negative criticism of the actions.
[COMMENT6]How many are arrested gives information about the level of disruption, so we start a disruption block again.
[COMMENT7]Still in a disruption block because this is clearly information about which newspapers may have been affected by the disruption.
[COMMENT8]Still obviously about the disruption so still inside the disruption content block.
[COMMENT9]I ended the disruption block here because although the vans were used to cause disruption, the information about what they were “covered with” doesn’t tell us anything more about the disruption itself.
[COMMENT10]Note the messaging block ends here because the sentence following the banners is also reporting on the protesters’ reasons for the protest, which is definitely also part of their messaging. But again, the Johnson quote is neither providing details of the disruption nor the protesters messaging – but it is a negative criticism block.
[COMMENT11]Starting a disruption block here because the picture and the caption are about the disruption, in the same way that the previous picture was.
[COMMENT12]I considered not including this in the disruption block because information about what police do is not necessarily about the details of disruption, but I left it in because the police came because of the disruption and because police being required to attend to deal with disruption is itself part of the disruption.
[COMMENT13]The next bit is only about protesters messaging so the disruption block ends here.
[COMMENT14]The entire paragraph was clearly about the protesters’ messaging.
[COMMENT15]Note, I didn’t include this first bit of the title in the disruption content block as this part of it doesn’t tell us anything about the disruption.
[COMMENT16]I justify the inclusion of the picture in the same way as in the previous article.
[COMMENT17]I ended the disruption block here because although everything till now (including picture and caption) has been detailing the disruptive acts, the details of the occupations of the protesters doesn’t tell us about the disruption they carried out.
[COMMENT18]I’m no longer commenting on choices that are by now (I hope) obvious.
[COMMENT19]Note that this is a messaging block because it is messages protesters are trying to convey. Although it expresses approval of the action, it is not coded as an approval of the protest block, because that needs to be expressed by anyone except the protesters themselves
[COMMENT20]This block represented a rather extreme example of negative comment on the protesters, as the expression of "furious" sentiment involved the protesters being rammed and chased.  
[COMMENT21]Note the careful positioning of the #NS tag so that the “verdict [being] seen as a triumph by environmental activists” is not included in a negative criticism block. The “triumph” phrase is not including in an approval block because it is an expression from activists themselves.
[COMMENT22]Note that actions reported as planned count in the same way as is they have happened.
[COMMENT23]Note, this messaging block begins while in a disruption block, because the threat to disrupt unless demands are met is both part of messaging and part of a description of disruption
[COMMENT24]I didn’t put this in a disruption block because it’s not clear whether these conditions relate to anything that was actually planned or happened.


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
End of article for tagging. Now respond with the entire article in its original format exactly as I provided it, except with the addition of tags, as appropriate. 
"""

have_another_go_no_error_prompt = """
Occasionally mistakes are made. The formatting of your tagging is correct - good - but sometimes the wrong content is tagged. Please check your previous output for compliance to the rules of this tagging task. If you have made any mistakes, please produce new output that corrects the mistakes. If you have not made any mistakes, please repeat the previous output. Note that being given an opportunity to make corrections does not imply you have made mistakes.
"""

have_another_go_after_error_prompt = """
Occasionally mistakes are made. There is indeed a format error in your tagging. It's also possible the wrong content is tagged, but this has not been checked and it may be correct. Please check your previous output for compliance to the rules of this tagging task and produce new output that corrects the mistakes. The error that your tagging has raised is:
"""

import json
import llmproc_core as llm
import datetime
import os
from bs4 import BeautifulSoup, Comment
import re
import warnings

client = llm.load_client()
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
llm_system_instruction = ""

warning_log_filename = f"warnings_{timestamp}.log"

def custom_formatwarning(message, category, *_args, **_kwargs ):
    formatted_warning = f"{datetime.datetime.now()}: {category.__name__}: {message}\n"
    with open(warning_log_filename, 'a') as log_file:
        log_file.write(formatted_warning)
    return formatted_warning

warnings.formatwarning = custom_formatwarning

def llm_tag_first_go(article):
    article_string = reconstitute_article_string(article)
    prompt = tag_instructions_prompt_intro + article_string + tag_instructions_prompt_end
    return llm.send_prompt(prompt)

def llm_tag_second_go_after_error(article):
    return llm_tag_second_go( article, have_another_go_after_error_prompt + article["tag_error_message"] )

def llm_tag_second_go_no_error(article):
    return llm_tag_second_go( article, have_another_go_no_error_prompt )

def llm_tag_second_go(article, have_another_go_prompt):
    article_string = reconstitute_article_string(article)
    original_prompt = tag_instructions_prompt_intro + article_string + tag_instructions_prompt_end
    return llm.send_prompt(have_another_go_prompt, prior_prompt = original_prompt, prior_llm = article["tag_first_go"])

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

def parse_articles_from_html_directory(directory_path):
    coded_articles = {}

    # Process all HTML files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.html'):
            filepath = os.path.join(directory_path, filename)

            # Extract source from filename (everything before first underscore)
            source = filename.split('_')[0] if '_' in filename else 'Unknown'

            with open(filepath, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract article ID from HTML comment
            article_id = None
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                id_match = re.search(r'Article ID:\s*(.+)', comment.strip())
                if id_match:
                    article_id = id_match.group(1)
                    break

            if not article_id:
                print(f"Warning: No article ID found in {filename}")
                continue

            current_article = {
                'id': article_id,
                'source': source
            }

            # Extract title from h1
            h1_tag = soup.find('h1')
            if h1_tag:
                current_article['title'] = h1_tag.get_text(strip=True)
                title_word_count = len(current_article['title'].split())
            else:
                print(f"Warning: No title (h1) found for article {article_id}")
                title_word_count = 0

            # Extract subtitle from h2
            h2_tag = soup.find('h2')
            subtitle_word_count = 0
            if h2_tag:
                current_article['subtitle'] = h2_tag.get_text(strip=True)
                subtitle_word_count = len(current_article['subtitle'].split())

            # Extract content
            content_lines = []

            # Find the main content area (everything after h1 and h2)
            # Start processing after the h2 (or h1 if no h2)
            start_tag = h2_tag if h2_tag else h1_tag

            if start_tag:
                for element in start_tag.find_next_siblings():
                    if element.name == 'p':
                        # Process paragraph text
                        text = element.get_text(strip=True)
                        if text:
                            content_lines.append(text)

                    elif element.name == 'figure':
                        # Process images with captions
                        img = element.find('img')
                        figcaption = element.find('figcaption')

                        if img and figcaption:
                            caption_text = figcaption.get_text(strip=True)
                            alt_text = img.get('alt', '')  # Get alt text if it exists
                            # Combine caption and alt text if both exist
                            if alt_text and alt_text != caption_text:
                                combined_text = f"{caption_text} (Alt: {alt_text})"
                            else:
                                combined_text = caption_text
                            content_lines.append(f'#PH #CS {combined_text} #CE')

            # Join content lines and count words
            content_word_count = 0
            if content_lines:
                current_article['main_content'] = '\n'.join(content_lines)
                # Count words in content, excluding image placeholder tags
                for line in content_lines:
                    if not line.startswith('#PH'):
                        content_word_count += len(line.split())
                    else:
                        # Count words in caption (between #CS and #CE)
                        caption_match = re.search(r'#CS (.+?) #CE', line)
                        if caption_match:
                            content_word_count += len(caption_match.group(1).split())

            # Add to coded_articles dictionary
            coded_articles[article_id] = current_article

            # Print parsing summary
            print(f"Parsed HTML file for {article_id}, title {title_word_count}, "
                  f"subtitle {subtitle_word_count}, content {content_word_count}")

    return coded_articles

class InvalidTagNestingErrorBatch3Style(Exception):
    """Custom exception for invalid tag nesting"""
    pass

def ensure_tags_have_spaces(content):
    """Ensure all tags are properly separated by spaces."""
    for tag in ['#DS', '#DE', '#PS', '#PE', '#MS', '#ME', '#AS', '#AE', '#NS', '#NE', '#PH', '#CS', '#CE']:
        content = content.replace(tag, f' {tag} ')
    return content

def analyze_content_for_batch_3_style(content):
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
                    raise InvalidTagNestingErrorBatch3Style("Nested messaging blocks are not allowed")
                messaging_depth += 1
            elif word == '#ME':
                if messaging_depth == 0:
                    raise InvalidTagNestingErrorBatch3Style("Found #ME without matching #MS")
                messaging_depth -= 1
            elif word == '#DS':
                if disruption_depth > 0:
                    raise InvalidTagNestingErrorBatch3Style("Nested disruption blocks are not allowed")
                disruption_depth += 1
            elif word == '#DE':
                if disruption_depth == 0:
                    raise InvalidTagNestingErrorBatch3Style("Found #DE without matching #DS")
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
        raise InvalidTagNestingErrorBatch3Style("Unclosed messaging block at end of content")
    if disruption_depth > 0:
        raise InvalidTagNestingErrorBatch3Style("Unclosed disruption block at end of content")
    return stats


class InvalidTagNestingError(Exception):
    """Custom exception for invalid tag nesting"""

    def __init__(self, message, word_list=None, error_position=None):
        super().__init__(message)
        self.word_list = word_list
        self.error_position = error_position

    def get_context(self):
        if self.word_list is None or self.error_position is None:
            return None
        start = max(0, self.error_position - 10)
        end = min(len(self.word_list), self.error_position + 11)
        return self.word_list[start:end]


def analyze_content(content):
    """Analyze content with multiple block types."""
    # Define block types and their tags
    block_types = {
        'general_disruption': {'start': '#DS', 'end': '#DE'},
        'protester_messaging': {'start': '#MS', 'end': '#ME'},
        'positive_comments': {'start': '#PS', 'end': '#PE'},
        'negative_comments': {'start': '#NS', 'end': '#NE'}
    }

    # Special tags that don't define blocks
    special_tags = {'#PH', '#CS', '#CE'}

    # Initialize statistics
    stats = {'total_words': 0, 'total_pictures': 0}
    for block_type in block_types:
        stats[f'{block_type}_words'] = 0
        stats[f'{block_type}_pictures'] = 0

    # Prepare content
    content = ensure_tags_have_spaces(content)

    # Add spaces around punctuation to prevent word merging (for some reason the LLM is sometimes omitting whitespace)
    # BUT preserve (Alt: pattern for alt text detection
    content = re.sub(r'(?<!\(Alt)([.,!?;:)])', r' \1', content)  # Space before punctuation, except after (Alt
    content = re.sub(r'\((?!Alt:)', r'( ', content)  # Space after opening paren, except for (Alt:
    content = re.sub(r'\s+', ' ', content)  # Normalize multiple spaces

    words = content.split()

    # Track depth of each block type
    block_depths = {block_type: 0 for block_type in block_types}

    # Track caption and alt text state
    in_caption = False
    in_alt_text = False

    # Process words
    for i, word in enumerate(words):
        # Handle caption tags
        if word == '#CS':
            in_caption = True
            continue
        elif word == '#CE':
            in_caption = False
            in_alt_text = False  # Reset alt text flag when leaving caption
            continue

        # Detect alt text within captions
        if in_caption:
            if word.startswith('(Alt:'):
                in_alt_text = True
            if in_alt_text and word.endswith(')'):
                in_alt_text = False
                continue  # Skip the closing word with )
            if in_alt_text:
                continue  # Skip all words inside alt text

        if word in special_tags:
            if word == '#PH':
                stats['total_pictures'] += 1
                for block_type, depth in block_depths.items():
                    if depth > 0:
                        stats[f'{block_type}_pictures'] += 1
            continue

        # Check if it's a block tag
        is_tag = False
        for block_type, tags in block_types.items():
            if word == tags['start']:
                if block_depths[block_type] > 0:
                    raise InvalidTagNestingError(
                        f"Nested {block_type} blocks are not allowed",
                        words,
                        i
                    )
                block_depths[block_type] += 1
                is_tag = True
                break
            elif word == tags['end']:
                if block_depths[block_type] == 0:
                    raise InvalidTagNestingError(
                        f"Found end tag without matching start tag for {block_type}",
                        words,
                        i
                    )
                block_depths[block_type] -= 1
                is_tag = True
                break

        # Word is not a tag, count it if it contains letters (and not just punctuation)
        if not is_tag and re.search(r'[a-zA-Z]', word):
            stats['total_words'] += 1

            # Then check which specific blocks it belongs to
            for block_type, depth in block_depths.items():
                if depth > 0:
                    stats[f'{block_type}_words'] += 1

    # Check for unclosed blocks
    for block_type, depth in block_depths.items():
        if depth > 0:
            raise InvalidTagNestingError(
                f"Unclosed {block_type} block at end of content",
                words,
                len(words) - 1
            )

    return stats



def count_words_in_tagged_blocks(article):
    for field in ['title', 'subtitle', 'main_content']:
        if field in article and article[field]:
            try:
                article[field + '_analysis'] = analyze_content(article[field])
            except InvalidTagNestingError as e:
                warnings.warn(f"Error in tags for article {article["id"]}.")
                article[field + '_analysis'] = f"Error in {field}: {str(e)}"
                article["tag_error"] = "present"

                context = e.get_context()
                print(f"Error: {str(e)}")
                print(f"Context: {' '.join(context)}")

def move_tags_to_main_fields(articles, which_go):
    output_path = f"tmp_{timestamp}_{which_go}.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        for article in articles.values():
            f.write(article.get(which_go, f"ERROR: tagging {which_go} not found")+"\n")
    return parse_articles_file(output_path)

def write_word_counts_file_for_batch_3_style(articles, append_file=""):
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


def write_word_counts_file(articles, append_file="", output_folder = "output_folders/article_content_block_word_counts/"):
    output_path = f'{output_folder}block_word_counts_{append_file}.tsv'

    # Define block types
    block_types = ['total', 'general_disruption', 'protester_messaging', 'positive_comments', 'negative_comments']

    # Define content sections and their stat types
    content_sections = {
        'title': ['words'],
        'subtitle': ['words'],
        'main_content': ['words', 'pictures'],
        'all_content': ['words', 'pictures', 'words_and_pictures']
    }

    # Build header
    header = ['id']
    for section, stat_types in content_sections.items():
        for block in block_types:
            for stat_type in stat_types:
                header.append(f'{section}_{block}_{stat_type}')
    header.append('tagging_error')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\t'.join(header) + '\n')

        for article_id, article in articles.items():
            row = [article_id]

            # Get analysis dicts
            analyses = {
                'title': article.get('title_analysis', {}),
                'subtitle': article.get('subtitle_analysis', {}),
                'main_content': article.get('main_content_analysis', {})
            }

            # Ensure all are dicts
            for key in analyses:
                if not isinstance(analyses[key], dict):
                    analyses[key] = {}

            # Process title, subtitle, main_content
            for section in ['title', 'subtitle', 'main_content']:
                for block in block_types:
                    for stat_type in content_sections[section]:
                        key = f'{block}_{stat_type}'
                        row.append(str(analyses[section].get(key, 0)))

            # Process all_content (combined)
            for block in block_types:
                words = sum(analyses[s].get(f'{block}_words', 0) for s in ['title', 'subtitle', 'main_content'])
                pictures = analyses['main_content'].get(f'{block}_pictures', 0)
                words_and_pictures = words + (pictures * 50)

                row.extend([str(words), str(pictures), str(words_and_pictures)])

            row.append(article.get('tagging_error', 'no'))
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


def apply_manual_corrections(articles_with_second_tagging, corrections_file_path, output_folder):
    articles_with_second_tagging_plus_corrections = articles_with_second_tagging.copy()
    manually_corrected_articles = parse_articles_file(corrections_file_path)

    # Replace articles that had tagging errors with corrected versions
    for article_id, original_article in articles_with_second_tagging.items():
        if original_article.get("tagging_error") == "yes":
            # Look for a corrected version
            if article_id in manually_corrected_articles:
                print(f"Applying manual corrections for article: {article_id}")
                corrected_article = manually_corrected_articles[article_id].copy()

                # Recompute word counts for the corrected article
                count_words_in_tagged_blocks(corrected_article)

                # Set tagging error to "no" since it's been manually corrected
                corrected_article["tagging_error"] = "no"

                # Replace in the output dictionary
                articles_with_second_tagging_plus_corrections[article_id] = corrected_article
            else:
                print(f"PROBLEM: No manual correction found for article with tagging error: {article_id}")

    write_word_counts_file(articles_with_second_tagging_plus_corrections, "corrected", output_folder )

def count_vanessa_batch_3():
    articles_for_counting = parse_articles_file('Formatted_Articles_20241118_195911 (Vanessa_Coding_50_corrected).txt')
    #articles_for_counting = parse_articles_file('Formatted_Articles_20241118_195911 (Vanessa_Coding_30_corrected).txt')
    for article in articles_for_counting.values():
        count_words_in_tagged_blocks(article)
    with open('human_coded_content_blocks.json', 'w') as f:
        json.dump(articles_for_counting, f, indent=4)
    write_word_counts_file(articles_for_counting, "assistant")

def count_batch_5_example():
    articles_for_counting = parse_articles_file('batch_5_example_for_testing_word_counts.txt')
    print( "Hello" )
    print(articles_for_counting)
    for article in articles_for_counting.values():
        count_words_in_tagged_blocks(article)
    #with open('human_coded_content_blocks.json', 'w') as f:
    #    json.dump(articles_for_counting, f, indent=4)
    write_word_counts_file(articles_for_counting, "assistant")


def llm_code_and_count_old():
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


def llm_code_and_count(
        directory_to_process = "../coding_batches/batch6/individual_articles/specific_and_edited",
        do_manual_corrections = True,
        output_folder = f'output_folders/article_content_block_word_counts/',
        corrections_file = "../coding_batches/batch6/individual_articles/specific_and_edited_block_tagging_manual_corrections/tagged_content_manually_corrected.txt"
    ):
    articles_for_coding = parse_articles_from_html_directory( directory_to_process )
    output_file = f"{output_folder}/article_content_block_word_counts_LLMResponses.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        articles_with_first_tagging = {}
        articles_with_second_tagging = {}
        for article in articles_for_coding.values():
            f.write("\nProcessing " + article["id"] + '\n')
            article["tag_first_go"] = llm.process_with_cache(llm_tag_first_go, article)
            f.write("\nFIRST LLM OUTPUT\n" + article["tag_first_go"] + '\n')
            article_with_first_tagging = parse_article_from_tag_string(article["tag_first_go"])
            count_words_in_tagged_blocks(article_with_first_tagging)

            if article_with_first_tagging.get("tag_error", "") == "present":
                f.write("\nFirst round: TAGGING ERROR(S) DETECTED\n")
                attach_tagging_error_to_original_article(article, article_with_first_tagging)
                # Add the specific error details to the log
                if "tag_error_message" in article:
                    f.write("Error details:\n" + article["tag_error_message"] + '\n')
                article_with_first_tagging["tagging_error"] = "yes"
                article["tag_second_go"] = llm.process_with_cache(llm_tag_second_go_after_error, article)
            else:
                f.write("\nFirst round: No tagging errors detected\n")
                article_with_first_tagging["tagging_error"] = "no"
                article["tag_second_go"] = llm.process_with_cache(llm_tag_second_go_no_error, article)

            articles_with_first_tagging[article_with_first_tagging["id"]] = article_with_first_tagging

            f.write("\nSECOND LLM OUTPUT\n" + article["tag_second_go"] + '\n')
            article_with_second_tagging = parse_article_from_tag_string(article["tag_second_go"])
            count_words_in_tagged_blocks(article_with_second_tagging)

            if article_with_second_tagging.get("tag_error", "") == "present":
                f.write("\nSecond round: TAGGING ERROR(S) DETECTED\n")
                attach_tagging_error_to_original_article(article, article_with_second_tagging)
                # Add the specific error details to the log
                if "tag_error_message" in article:
                    f.write("Error details:\n" + article["tag_error_message"] + '\n')
                article_with_second_tagging["tagging_error"] = "yes"
            else:
                f.write("\nSecond round: No tagging errors detected\n")
                article_with_second_tagging["tagging_error"] = "no"

            articles_with_second_tagging[article_with_second_tagging["id"]] = article_with_second_tagging

        with open('llm_coded_content_blocks.json', 'w') as f:
            json.dump(articles_with_second_tagging, f, indent=4)
        write_word_counts_file(articles_with_first_tagging, "first", output_folder )
        write_word_counts_file(articles_with_second_tagging, "second", output_folder )
        if do_manual_corrections:
            apply_manual_corrections(articles_with_second_tagging, corrections_file, output_folder )


def main():
    llm_code_and_count(
        "../coding_batches/batch7/batch7_individual_articles/owe_specific/production/",
        True,
        "../coding_batches/batch7/batch7_individual_articles/owe_specific/word_count_output/",
        "../coding_batches/batch7/batch7_individual_articles/owe_specific/word_count_output/corrections.txt"
    )
    #llm_code_and_count()
    #count_vanessa_batch_3()
    #count_batch_5_example()

if __name__ == "__main__":
    main()
