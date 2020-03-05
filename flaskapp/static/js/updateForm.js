{/* <form method="POST" action="{{ url_for('receive_shell') }}" enctype="multipart/form-data">
<div class="form-group">
    {{ form.csrf_token }}
    {{ form.sender.label() }}
    {{ form.sender(class='custom-select', id='sender') }}
</div>
<div class="form-group">
    {{ form.pattern.label() }}
    {{ form.pattern(class='custom-select', id='pattern') }}
</div>
<div class="form-group">
    {{ form.conditions.label() }}
    {{ form.conditions(class='custom-form', id='conditions') }}
</div>
<div class="form-group mt-4">
    <input type="submit" value="Create shell" class="btn btn-primary">
    <a href="#" class="btn btn-danger">Cancel</a>
</div>
</form> */}

// This script updates the pattern select field in above form in create_recv_shell.html based on selected sender in sender select field.
function updateForm(selectObj) {
    sender = selectObj.value;
    fetch('/receive_shell/' + sender).then(function(response){
        response.json().then(function(data){
            // update condition options
            let conditionOptions = "";
            for (let c of data.conditions) {
                conditionOptions += '<div class="card">\
                <div class="card-header">\
                    <input type="checkbox" name="conditions" value="'+c[0][1]+'">\
                    <label for="'+c[0][0]+'" class="card-link" data-toggle="collapse" href="#collapseDesc'+c[0][0]+'">'+c[0][1]+'</label>\
                </div>\
                <div id="collapseDesc'+c[0][0]+'" class="collapse" data-parent="#accordion-body">\
                    <div class="card-body">\
                    Description:<br>\
                    '+c[2]+'\
                    </div>\
                </div>\
            </div>'
            }
            document.getElementById('accordion-body').innerHTML = conditionOptions;
        });
    });
}

$("#Pay").on("change", function() {
    $("#payment_amount").toggle();
});