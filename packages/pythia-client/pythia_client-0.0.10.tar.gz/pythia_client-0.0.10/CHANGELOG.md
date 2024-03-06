#### v0.0.10
- Fix Schema to make score optional (Qdrant compatibility).  Compatible with `haystack-api` v0.0.5
- 
#### v0.0.9
- `index_files` now return a simple json indicating that the background indexation task have been acception. New `get_indexing_jobs` function take an `owner` value as parameters and return the top 20 most recent indexation job and their results or status. New optional `owner` parameter for the query endpoint to indicate which user sent the message in the DynamoDB table log. Compatible with `haystack-api` v0.0.5

#### v0.0.8
- NEW: New optional parameter `chat_history` in the `.query()` method. It allows to add previous exchange with the LLM to the new query. Chat History must follow the ChatMessages format (dict containing: content, role, name, meta), see https://docs.haystack.deepset.ai/v2.0/docs/data-classes#chatmessage
- Compatible with `haystack-api` v0.0.4

#### v0.0.7
- New response Schema for the Haystack-API after version bump and removal of LiteLLM.

#### v0.0.6
- Added the new parameter `return_content` to the `list_docs` method. The method `list_docs` now by default doesn't return document content (to save on bandwidth). Set `return_content` to `True` to return the content of the documents.  

#### v0.0.5
- Initial Release. Compatible with `haystack-api` v0.0.1