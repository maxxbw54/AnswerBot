# answerbot-tool

## tables
a. **posts**

Imported from SO data dump.

b. **java**

Select all posts tagged as Java in posts.

c. **repo**

Preprocess all the posts in java
If one post is a question, then, .
If one post is an answer, then, . 

Attributes,
1. Id.
2. PostTypeId. (1 = Question, 2 = Answer)
3. Title (ONLY for question)
4. Title-clean (ONLY for question. Stop words removal and stemming)
5. Body
6. Body-clean (clean html, )