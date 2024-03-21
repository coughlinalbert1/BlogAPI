from typing import List, Optional, Annotated
from fastapi import APIRouter, Header
from fastapi.responses import Response, HTMLResponse, PlainTextResponse

router = APIRouter(
    prefix='/product',
    tags=['product']
)

products = ['watch', 'camera', 'laptop', 'phone', 'tablet']

@router.get('/all')
def get_products():
    data = ' '.join(products)
    return Response(content=data, media_type='text/plain')

@router.get('/withheader')
def get_products_with_header(
    custom_header: Optional[List[str]] = Header(None) # for multiple custom headers
):
    headers = {}
    headers['custom_response_header'] = ", ".join(custom_header)
    
    return PlainTextResponse(', '.join(products), headers=headers)


@router.get('/{id}', responses={
    404: {
        "content": {
            "text/html": {
                "example": "<div class='product'>watch</div>"
            }
        },
        "description": "A clear text error message"
    },
    200: {
        "content": {
            "text/html": {
                "example": "<div class='product'>watch</div>"
            }
        },
        "description": "Returns the HTML for an object"
    }
})
def get_product(id: int):
    if id > len(products):
        return PlainTextResponse(content='Product not found', media_type='text/plain')
    else:
        product = products[id]
        out = f'''
        <head>
            <style>
                .product {{
                    width: 500px;
                    height: 30px;
                    background-color: lightblue;
                    border: 2px inset green;
                    text-align: center;
                }}
            </style>
        </head>
        <div class="product">{product}</div>
        '''
        return HTMLResponse(content=out, media_type='text/html')

