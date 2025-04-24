#This wouldn't actually run because you'd need an anthropic key specified
#This was run again a second time but with output_only_articles_passing_screening=Truecd

import llm_activism_article_multitool as multitool

import os
os.chdir("working_temp")

if __name__ == "__main__":
    multitool.process_articles(
        key = anthropic_key,
        use_owe_focussed=False,
        articles_path="../article_contents",
        count_type="pass_screening",
        stop_after=150,
        article_selection="random_weighted",
        process_only_selected=True,
        article_order_random_seed=430,
        do_screening=True,
        do_summarising=True,
        output_article_summarised=True,
        output_only_articles_passing_screening=False,
        output_articles_individually=True,
        suppress_id_in_html=True,
        coding_output_filename="batch6_llm_screening.tsv",
        html_output_filename="batch6_html_output.html",
        article_exclusion_list=["../coding_batches/batch2/batch2_random_selection.txt",
                                "../coding_batches/batch3/batch3_random_selection.txt"]
    )