from marshmallow import Schema, fields, post_load, validate

from app.models.post import Post


class PostSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String()
    description = fields.String(required=True)
    priority = fields.Integer(validate=validate.Range(min=1))
    # created_at = fields.DateTime(required=True)

    @post_load
    def make_post(self, data, **kwargs):
        return Post(**data)
