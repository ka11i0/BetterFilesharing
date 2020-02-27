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
            // update pattern options
            let conditionOptions = "";
            for (let pat of data.conditions) {
                conditionOptions += '<option value="'+pat.shell_id+'">'+pat.pattern+'</option>';
            }
            document.getElementById('pattern').innerHTML = conditionOptions;
        });
    });
    // TODO: update the condition select field
}