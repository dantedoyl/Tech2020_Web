$('.js-vote').click(function(ev){
    ev.preventDefault()
    var $this = $(this)
    let str = this.id
    if (str.indexOf('question') != -1)
        str = 'question'
    else
        str = 'answer'
    action = $this.data('action')
    id=$this.data('id')
    $.ajax('/vote/',{
        method: 'POST',
        data: {
            type: str,
            action: action,
            id: id,
        },
    }).done(function(data) {
        document.getElementById(data['type']+'_rating_' + data['id']).innerHTML = data['rating']
        document.getElementById(data['type']+'_dislike_'+ data['id']).style.color = "darkgray"
        document.getElementById(data['type']+'_like_'+ data['id']).style.color = "darkgray"
        document.getElementById(data['type']+'_dislike_'+ data['id']).style.pointerEvents = "none"
        document.getElementById(data['type']+'_like_'+ data['id']).style.pointerEvents = "none"
        document.getElementById(data['type']+'_'+data['action']+'_'+ data['id']).style.color = "#ff0000"
    });
})

$('.js-correct').click(function(ev){
    ev.preventDefault()
    var $this = $(this)
    // action = $this.data('action')
    id=$this.data('id')
    $.ajax('/correct/',{
        method: 'POST',
        data: {
            id: id,
        },
    }).done(function(data) {
        document.getElementById('answer_check_' + data['id']).checked = !document.getElementById('answer_check_' + data['id']).checked
    });
})