import warnings
warnings.warn("Using the version of the OWE prompts that does not mention tax and school strikes. We may want to update that. Also think about animal rights: https://docs.google.com/document/d/1vlhulnQNw0ANMgdldv6uZTnFujewdkNnn9NQraw5or8/edit?tab=t.0", UserWarning)

screening_code_names = ["OWE", "SPURIOUS", "SPECIFIC", "LETTER", "ROUNDUP", "NON-UK EDITION", "NON-ENGLISH", "VIDEO", "NON-DISRUPTIVE OWE"]

rating_code_names_b2 = ["Number of protestors", "Target category", "Activity being deliberately disrupted", "Activity being accidentally disrupted", "Nature of disruption", "Visual appearance costumes", "Visual appearance not ordinary", "Demographics", "Demand", "Location", "Acceptance of protest", "Believe in general acceptability", "Believe in general unacceptability", "Protester demographic diversity", "Radicalness of demand", "Level of disruption", "Otherness", "Political slant", "Issue bundling", "Portrayal", "Attention to message", "Attention to disruption" ]

rating_code_names = ["Level of disruption, Business damaging", "Level of disruption, Business non-damaging", "Level of disruption, Individual responsible", "Level of disruption, Government or authority", "Level of disruption, Public everyday", "Level of disruption, Public damaging", "Level of disruption, Caring", "Level of disruption, Culture or sport", "Clarity, Otherness", "Otherness", "Portrayal", "Attention to message", "Attention to disruption", "Clarity, Number of Protesters", "Number of protesters", "Activity being deliberately disrupted", "Activity being accidentally disrupted", "Nature of disruption", "Clarity, Visual appearance", "Visual appearance costumes", "Visual appearance not ordinary", "Demographics", "Demand", "Location" ]

prompt_summarise_intro = """Please process a news media article for me. The article contains some information about a disruptive primary protest action taken by one or more environmental protesters. The primary protest action is the most prominent environmental protest action mentioned in the article that is disruptive. The primary protest action is not action that is not disruptive. The article may or may not also contain information about secondary separate actions taken by one or more protesters. I would like you to produce a summarised version of the whole article, containing as much information as possible about the primary disruptive protest action, using the same wording as the original, but with no information about any secondary protest actions. 

Make sure your summary contains the following information, if the information is also present in the article: the number of people involved in the protest, the target of the disruption (e.g. a company or government building), the jobs or backgrounds of the protesters, and the demands of the protesters. Try to preserve the tone of the article (positive or negative towards the protests). The summary should itself be plausible as an article, so it should not (for example) make reference to the original article. 

The target word count is 300 words.

Here is the original article:
"""

prompt_summarise_intro_old = """Please process a news media article for me. The article contains some information about a disruptive primary protest action taken by one or more environmental protesters. The primary protest action is the most prominent disruptive environmental protest action mentioned in the article. The article may or may not also contain information about secondary separate actions taken by one or more protesters. I would like you to produce a summarised version of the whole article, containing as much information as possible about the primary protest action, using the same wording as the original, but with no information about any secondary protest actions. 

Make sure your summary contains the following information, if the information is also present in the article: the number of people involved in the protest, the target of the disruption (e.g. a company or government building), the jobs or backgrounds of the protesters, and the demands of the protesters. Try to preserve the tone of the article (positive or negative towards the protests).

The target word count is 300 words.

Here is the original article:
"""

prompt_summarise_end = "\nThe article ends here.\nNow output the summarised article, beginning with the article title."

prompt_summarise_end_old = "\nThe article ends here.\nNow output the summarised article. Do not output anything except the summarised article (no pre-amble). Begin with the article title (without summarising it)."

prompt_resummarise_intro = "A previous instance of yourself has summarised a news media article. It has also answered some questions about the original article and the summarised article. The purpose of the questions are to examine whether certain key characteristics of the original article are preserved in the summarised article. However, the answers to some of the questions were different between the original and the summarised article. Please resummarise the article. By resummarise I mean examine the summarised version, consider why the summarising process might have changed the answers to one or more questions, and change the summary so that the answers to the questions regarding the resummarised article are more likely to match the answers to the questions regarding the original article. Here is the original article:\n"

prompt_resummarise_link1 = "\nHere is the summarised article:\n"

prompt_resummarise_link2 = """\nBelow are the answers to the questions. These answers are in a TSV table with three columns. The first column contains the questions. The second column contains the answers regarding the original article. The third column contains the answers regarding the summarised article. The fourth column contains the word "match" if the answers match and the word "MISMATCH" if the answers do not match.\n"""

prompt_resummarise_end = "\nNow please produce the resummarised article, adjusting the summarised article to address the mismatches between the original and the summarised versions mentioned in the table above. Any material you now incorporate must come entirely from the original article. Newly incorporated material may be summarised from the original but you must not create new material simply to address mismatches. Do not output anything except the resummarised article (no pre-amble). "

prompt_owe_intro = """
Your task is to screen a news media article to determine if it meets a specific definition. The definition is called OWE and it might apply or not apply to the article. Before I can define what it means for an article to be OWE I need to make some further definitions.

Disruptive protest is protest that appears to be aimed at disrupting the functioning of some other activity generally regarded as legitimate (whether that is fossil fuel operations, road transport, sport, government operations, cultural displays, etcetera) as a means to draw attention to a cause or as a means to prevent the activity. Disruption is not dependent on the actual scale of disturbance of economic or social life.

For example, a registered march in a city can cause great inconvenience, but because the disruption is a side-effect of the marchers’ primary intention to amplify their communications by gathering in numbers, we do not regard this as disruptive protest. Protest conducted by groups that often disrupt is not inherently disruptive. Such groups sometimes protest in ways that superficially resemble their disruptive protests without intending to disrupt on that occasion.

Environmental protest is protest about issues that are uncontroversially serious environmental problems according to mainstream-science influenced positions. Therefore, protests against (for example) wind-turbines or mobile data networks are not included.

OWE is defined by the following question. In a counterfactual world identical to ours, except that environmental protesters never used disruptive methods, would this article still exist in a form where the primary message was hardly changed? If the answer is "No", the article is OWE, because the article's primary message owes its existence in part to disruptive protest. Further guidance for judging OWE:
It is not allowed to assume that disruptive protest causes increased concern and thus causes articles to be written expressing concern about the environment.
Articles that are OWE may be only secondarily about protest - for example the focal issue may be about secondary consequences of protest, such as legislation about protest. They are still OWE as long as the article frames disruptive protest as a necessary cause of these secondary consequences. If the article frames a competing potential cause more prominently (e.g., protest about other issues), then it is not OWE.

Here is the article for you to judge:
"""

prompt_owe_end = "\nNow output a single word, which is Yes if the article is OWE, and No if the article is not OWE."

prompt_owe_specific_intro = """
Your task is to screen a news media article to determine if it meets a specific definition. The definition is called OWE_SPECIFIC and it might apply or not apply to the article. Before I can define what it means for an article to be OWE_SPECIFIC I need to make some further definitions.

Disruptive protest is protest that appears to be aimed at disrupting the functioning of some other activity generally regarded as legitimate (whether that is fossil fuel operations, road transport, sport, government operations, cultural displays, etcetera) as a means to draw attention to a cause or as a means to prevent the activity. Disruption is not dependent on the actual scale of disturbance of economic or social life.

For example, a registered march in a city can cause great inconvenience, but because the disruption is a side-effect of the marchers’ primary intention to amplify their communications by gathering in numbers, we do not regard this as disruptive protest. Protest conducted by groups that often disrupt is not inherently disruptive. Such groups sometimes protest in ways that superficially resemble their disruptive protests without intending to disrupt on that occasion.

Environmental protest is protest about issues that are uncontroversially serious environmental problems according to mainstream-science influenced positions. Therefore, protests against (for example) wind-turbines or mobile data networks are not included.

OWE_SPECIFIC is defined by the following question. In a counterfactual world identical to ours, except that environmental protesters had not used disruptive methods at one protest mentioned in the article (or a small number of multiple protests all closely linked in theme and time and protest method), would this article still exist in a form where the primary message was hardly changed? If the answer is "No", the article is OWE_SPECIFIC, because the article's primary message owes its existence in part to one or more specific disruptive protests.

Here is the article for you to judge:
"""

prompt_owe_specific_end = "\nNow output a single word, and only that single word, which is Yes if the article is OWE_SPECIFIC, and No if the article is not OWE_SPECIFIC."

prompt_full_screening_intro = """The following definitions of concepts (in capital letters) are relevant for judging some characteristics of a news media article, which is a task you will shortly perform.
1 OWE. An article may be OWE, indicating it owes its existence to disruptive environmental protest. Further definitions are required:
1a. Disruptive protest is protest that appears to be aimed at disrupting the functioning of some other activity generally regarded as legitimate (whether that is fossil fuel operations, road transport, sport, government operations, cultural displays, etcetera) as a means to draw attention to a cause or as a means to prevent the activity. Disruption is not dependent on the actual scale of disturbance of economic or social life. For example, a registered march in a city can cause great inconvenience, but because the disruption is a side-effect of the marchers’ primary intention to amplify their communications by gathering in numbers, we do not regard this as disruptive protest. Protest conducted by groups that often disrupt is not inherently disruptive. Such groups sometimes protest in ways that superficially resemble their disruptive protests without intending to disrupt on that occasion.
1b. Environmental protest is protest about issues that are uncontroversially serious environmental problems according to mainstream-science influenced positions. Therefore, protests against (for example) wind-turbines or mobile data networks are not included.
1c. OWE is defined by the following question. In a counterfactual world identical to ours, except that environmental protesters never used disruptive methods, would this article still exist in a form where the primary message was hardly changed? If the answer is "No", OWE is scored, because the article's primary message owes its existence in part to disruptive protest. Further guidance for scoring OWE:
1ci. It is not allowed to assume that disruptive protest causes increased concern and thus causes articles to be written expressing concern about the environment.
1cii. Articles that OWE may be only secondarily about protest - for example the focal issue may be about secondary consequences of protest, such as legislation about protest. They still OWE as long as the article frames disruptive protest as a necessary cause of these secondary consequences. If the article frames a competing potential cause more prominently (e.g., protest about other issues), then OWE is not scored.
2 SPURIOUS. Articles are SPURIOUS if they clearly have nothing to do with environmental protest (SPURIOUS implies definitely not OWE). An article might not score OWE but still not be SPURIOUS, for example if it was about protest legislation but focussed on other types of protest.
3 SPECIFIC. SPECIFIC articles mention at least one specific disruptive environmental protest.
4 LETTER. A LETTER article consists of one or more readers’ letters to the editor. These tend to be short, and this is not the same as a debate article, which tends to be longer.
5 ROUNDUP. A ROUNDUP article is a collection of short updates or links to other articles. These updates are often thematically related but the article as a whole is not a coherent single article of the type that would appear in a print edition.
6 NON-UK EDITION. NON-UK EDITION articles are marked as coming from non-UK editions.
7 NON-ENGLISH. A NON-ENGLISH article is an article in a language other than English (for example, the BBC has Welsh articles).
8 VIDEO. A VIDEO article is one primarily featuring one or more videos, i.e., there is no text in the article that is not video caption (serving a purpose of explaining the video).
9 NON_DISRUPTIVE OWE. An article is NON-DISRUPTIVE OWE if it is OWE, except with regard to environmental protest that has no disruptive element.

Here is the news media article that you will judge with regard to the above characteristics:
"""

prompt_full_screening_end = "\nNow judge the article for each of the above characteristics. Output a 9 by 2 table in TSV format, where the top row is each of the characteristics, and the bottom row contains, for each characteristic, Yes if the article has that characteristic, and No if the article does not."

prompt_coding_intro = """Your task is to answer a series of questions concerning a news media article, as if you were an intelligent but otherwise ordinary person from the United Kingdom. The questions are are of three different types. For questions of type TEXT, you are free to respond with any text that best answers the question. For questions of type MULTIPLE_CHOICE, you must response with one of the response options. For questions of type CHECKBOX, you may respond with as many of the response options as is appropriate, which could be none or all or something in between. Different response options are separated by semi-colons. When responding with multiple response options, separate them with semi-colons in the response. The questions are provided in TSV format, in four columns with a header row. Each row after the header defines one question. The Type column determines the type of the question. The Name column is the name of the question. The Question column is the question to answer. The Response options column contains the response options for that question. Here are the questions in TSV format:
"""

prompt_coding_link = "\nHere is the news media article:\n"

prompt_coding_end = "\nNow output answers to all of the questions concerning the news media article. Produce output in TSV format, in two columns, where each row corresponds to one question, with the first column contains the question names in the original order and the second column contains your response to each question.\n"
