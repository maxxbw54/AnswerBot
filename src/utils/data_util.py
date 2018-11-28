# -*- coding: UTF-8 -*-

# question unit
def preprocessing_for_SO_QuestionUnit(SO_QuestionUnit):
    SO_QuestionUnit.title = preprocessing_for_text_of_QuestionUnit(SO_QuestionUnit.title, 0)
    SO_QuestionUnit.desc = preprocessing_for_text_of_QuestionUnit(SO_QuestionUnit.desc, 1)
    SO_QuestionUnit.tag = preprocessing_for_tag(SO_QuestionUnit.tag)
    return SO_QuestionUnit


# question  unit tag
def preprocessing_for_tag(tag_str):
    return tag_str.replace('<', ' ').replace('>', ' ').replace('  ', ' ').strip()


# question unit title and description
def preprocessing_for_text_of_QuestionUnit(text, ifdesc):
    # description
    if ifdesc:
        text = delete_tag_content(text, "<pre><code>", "</code></pre>")
        text = reserve_content(text, "<a href=", "</a>")
        text = replace_html_tag_for_question(text)
        text = replace_useless_symbol(text)
    # title
    else:
        text = preprocessing_for_general_text(text)
    text = text.replace('?', ' ').replace('!', ' ')
    text = replace_double_space(text)
    return text.strip().lower()


# answer unit
def preprocessing_for_SO_AnswerUnit(SO_AnswerUnit):
    SO_AnswerUnit.desc = preprocessing_for_text_of_AnswerUnit(SO_AnswerUnit.desc)
    return SO_AnswerUnit


# answer unit
def preprocessing_for_text_of_AnswerUnit(text):
    text = delete_tag_content(text, "<pre><code>", "</code></pre>")
    text = delete_tag_content(text, "<img src=", ">")
    text = reserve_content(text, "<a href=", "</a>")
    text = replace_html_tag_for_answer(text)
    text = replace_useless_symbol(text)
    text = replace_double_space(text)
    text = preprocessing_for_general_text(text)
    return text.strip()


# example:
# <a href="http://en.wikipedia.org/wiki/Eclipse_%28software%29">Eclipse</a>
def reserve_content(text, tag_head, tag_tail):
    while tag_head in text:
        head_pos = text.find(tag_head)
        tail_pos = text.find(tag_tail)
        if head_pos >= tail_pos:
            break
        ahref_head = text[head_pos:tail_pos].find(">")
        ahref_content = text[head_pos + ahref_head + 1:tail_pos]
        text = text[:head_pos] + " " + ahref_content + " " + text[tail_pos + len(tag_tail):]
    return text


def delete_tag_content(text, tag_head, tag_tail):
    while tag_head in text:
        head_pos = text.find(tag_head)
        tail_pos = head_pos + text[head_pos:].find(tag_tail)
        if head_pos >= tail_pos:
            break
        text = text[:head_pos] + text[tail_pos + len(tag_tail):]
    return text


def preprocessing_for_general_text(text):
    # c++, c#
    text = replace_useless_symbol(text)
    text = replace_double_space(text)
    return text


def replace_double_space(text):
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text


def replace_html_tag_for_question(text):
    text = text.replace('&quot;', ' ').replace('&apos;', ' ').replace('&gt;', ' ').replace('<p>', ' ').replace(
        '<li>', ' ').replace('</li>', ' ').replace('<ol>', ' ').replace('</ol>', ' ').replace('<br>', ' ').replace(
        '<br/>', ' ').replace('<h2>', ' ').replace('</h2>', ' ').replace('<h3>', ' ').replace('</h3>', ' ').replace(
        '<b>', ' ').replace('</ul>', ' ').replace('</h3>', ' ').replace('&#xD;', ' ').replace('<hr>', ' ').replace(
        '<ul>', ' ').replace('</p>', ' ').replace('<code>', ' ').replace('</code>', ' ').replace('&lt;', ' ').replace(
        '&amp;', ' ').replace('<em>', ' ').replace('</em>', ' ').replace('<blockquote>', ' ').replace('</blockquote>',
                                                                                                      ' ').replace(
        '<a>',
        ' ').replace('</a>', ' ').replace('<i>', ' ').replace('</i>', ' ').replace('<s>', ' ').replace('</s>',
                                                                                                       ' ').replace(
        '&#xA', ' ').replace('<pre>', ' ').replace('</pre>', ' ')
    return text


# exclude <p> and </p>
def replace_html_tag_for_answer(text):
    text = text.replace('&quot;', ' ').replace('&apos;', ' ').replace('&gt;', ' ').replace('<li>', ' ').replace('</li>',
                                                                                                                ' ').replace(
        '<ol>', ' ').replace('</ol>', ' ').replace('<br>', ' ').replace('<br/>', ' ').replace('<h2>', ' ').replace(
        '</h2>', ' ').replace('<h3>', ' ').replace('</h3>', ' ').replace('<b>', ' ').replace('</b>', ' ').replace(
        '</ul>', ' ').replace(
        '</h3>', ' ').replace('&#xD;', ' ').replace('<hr>', ' ').replace(
        '<ul>', ' ').replace('<code>', ' ').replace('</code>', ' ').replace('&lt;', ' ').replace('&amp;', ' ').replace(
        '<em>', ' ').replace('</em>', ' ').replace('<blockquote>', ' ').replace('</blockquote>',
                                                                                ' ').replace('<a>', ' ').replace('</a>',
                                                                                                                 ' ').replace(
        '<i>', ' ').replace('</i>', ' ').replace('<s>', ' ').replace('</s>', ' ').replace('&#xA', ' ').replace('<br>',
                                                                                                               ' ')
    return text


def replace_useless_symbol(text):
    # don't use .replace('/', ' ')
    text = text.replace('{', ' ').replace('£', '').replace('}', ' ').replace('[', ' ').replace(']', ' ').replace('(',
                                                                                                                 ' ').replace(
        ')', ' ').replace(
        '+', ' ').replace('*', ' ').replace("n’t", " not").replace("n\'t", " not").replace("’ve", " have").replace(
        '\'ve', 'have').replace('I\'m', 'I am').replace("I\'d", "I would").replace("I\'ll", "I will").replace('\'s',
                                                                                                              ' is').replace(
        "’", " ").replace(',', '').replace(':', ' ').replace('-', '').replace('^', ' ').replace('\"', ' ').replace('\'',
                                                                                                                   ' ').replace(
        ';', ' ').replace('$', ' ').replace('`', ' ').replace('...', ' ').replace('..', ' ').replace('=', ' ').replace(
        '\\', ' ').replace('&', ' ').replace('@', ' ')
    return text


if __name__ == '__main__':
    text = 'text > <img src= http://i.stack.imgur.com/ltCod.    png alt= Rich task editor >   '
    print delete_tag_content(text, "<img src=", ">")
    print replace_double_space(text)
