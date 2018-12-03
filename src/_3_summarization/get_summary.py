from _3_summurization.MMR_Analysis import MMR_Analysis
import operator


def get_summary(query, top_ss, topk):
    selected_sentence = MMR_Analysis(query, top_ss, topk)
    # sort by q_id then order
    selected_sentence.sort(key=operator.itemgetter(5, 3), reverse=True)
    summary = ''
    for [sent_Num, raw_sent, sent_without_tag, Order, Score, q_id] in selected_sentence:
        summary += (str(sent_Num) + ' $$ ' + raw_sent.strip() + '\n')
    return summary
