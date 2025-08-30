from flask import Blueprint, jsonify
from app.models import Category

category_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@category_bp.route('', methods=['GET'])
def get_categories():
    #Get all categories
    try:
        categories = Category.query.order_by(Category.name.asc()).all()
        categories_data = [{'id': cat.id, 'name': cat.name} for cat in categories]
        
        return jsonify({
            'categories': categories_data
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    #Get a single category by ID
    try:
        category = Category.query.get_or_404(category_id)
        return jsonify({
            'category': category.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500