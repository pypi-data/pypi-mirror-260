from fastapi import Depends, APIRouter, HTTPException

from komodo.server.globals import get_appliance

router = APIRouter(
    prefix='/api/v1/appliance',
    tags=['Appliance']
)


@router.get('/description', response_model=dict, summary='Get appliance description',
            description='Get the description of the appliance.')
def get_appliance_description(appliance=Depends(get_appliance)):
    if not appliance:
        raise HTTPException(status_code=404, detail="Appliance not found")

    return {
        "shortcode": appliance.shortcode,
        "name": appliance.name,
        "purpose": appliance.purpose,
        "agents": [a.to_dict() for a in appliance.agents]
    }
