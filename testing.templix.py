
from GooBa import view, CreateElement

@view
def somepage():
    return (
<div>
        <span onclick="{document.getElementById('ticketModal').style.display='none'}" class="w3-button w3-teal w3-xlarge w3-display-topright">×</span>
        <button onclick="{document.getElementById('ticketModal').style.display='none'}" class="w3-button w3-red w3-section">Close <i class="fa fa-remove"></i></button>
</div>
)