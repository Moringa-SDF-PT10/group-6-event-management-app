from flask import Blueprint, jsonify, request
from app import db
from app.models.category import Category
from app.auth_decorators import role_required

category_bp = Blueprint("category_bp", __name__, url_prefix="/categories")

# ---------- PUBLIC ROUTES ----------

@category_bp.route("/", methods=["GET"])
def get_categories():
    """
    Get all categories.
    """
    categories = Category.query.order_by(Category.name.asc()).all()
    return jsonify([category.to_dict() for category in categories])

@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category_by_id(category_id):
    """
    Get a single category by its ID.
    """
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(category.to_dict())

@category_bp.route("/slug/<string:category_slug>", methods=["GET"])
def get_category_by_slug(category_slug):
    """
    Get a single category by its slug.
    """
    category = Category.query.filter_by(slug=category_slug).first()
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(category.to_dict())

# ---------- ADMIN/ORGANIZER ROUTES ----------

@category_bp.route("/", methods=["POST"])
@role_required(["organizer"])
def create_category():
    """
    Create a new category. Only accessible to organizers.
    """
    data = request.get_json()
    if not data or not "name" in data:
        return jsonify({"error": "Missing category name"}), 400

    name = data["name"]
    slug = Category.create_slug(name)

    if Category.query.filter_by(slug=slug).first():
        return jsonify({"error": "Category with this name already exists"}), 409

    new_category = Category(
        name=name,
        slug=slug,
        description=data.get("description")
    )
    db.session.add(new_category)
    db.session.commit()

    return jsonify({
        "message": "Category created successfully",
        "category": new_category.to_dict()
    }), 201

@category_bp.route("/<int:category_id>", methods=["PUT", "PATCH"])
@role_required(["organizer"])
def update_category(category_id):
    """
    Update an existing category. Only accessible to organizers.
    """
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400

    if "name" in data:
        category.name = data["name"]
        category.slug = Category.create_slug(data["name"])
    if "description" in data:
        category.description = data["description"]

    db.session.commit()
    return jsonify({
        "message": "Category updated successfully",
        "category": category.to_dict()
    })

@category_bp.route("/<int:category_id>", methods=["DELETE"])
@role_required(["organizer"])
def delete_category(category_id):
    """
    Delete a category. Only accessible to organizers.
    """
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"})