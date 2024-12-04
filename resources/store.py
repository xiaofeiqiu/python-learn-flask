import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import StoreModel
from schemas.store import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("stores", __name__, description="curd stores")


@blp.route("/store/<string:id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, id):
        store = StoreModel.query.get_or_404(id)
        return store

    def delete(self, id):
        store = StoreModel.query.get_or_404(id)
        db.session.delete(store)
        db.session.commit()
        return {"message": f"{id} deleted"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(store_data)
        try:
            db.session(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="already exist")
        except SQLAlchemyError:
            abort(500, message="error creating the store")

        return store
