
#Document(beanie): Entity + persistence
#pydantic model, persisted in MongoDB, automatic _id, has database methods: .save .get(id), .find()

#BaseModel (Pydantic): DTO (data transfer object)
# Validation only; used for request/response schemas (body validation)
    

class Comment(Document):
    user: Link[User]
    content: str

    class Settings:
        name = "comments"

class CommentParam(BaseModel):
    user: PydanticObjectId
    content: str

class Post(Document):
    title: str
    content: str
    user: Link[User]
    comments: list[Link[Comment]] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)

    class Settings:
        name = "posts"
        indexes = ["tags"]

class PostCreate(BaseModel): #diference BaseModel and Document? Used for request body validation? why?
    title: str
    content: str
    user: PydanticObjectId = Field(..., description="ID do usuário") #Clients send IDs, not database references. -> server converts it
    tags: list[str] = Field(default_factory=list) #user-provided input
    #why no comments? Are created later. by other users. stored in a separate collection

# 