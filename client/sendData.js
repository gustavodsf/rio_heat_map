//função que percorre os filtros e verifica quais parâmetros estão marcados para ser usado na consulta
function preencheFiltros(){
    var data = { 'filtros' : []};
    $("#filtros input:checked").each(function() {
      data['filtros'].push("&"+$(this).attr('name')+"="+$(this).val());
    });
    
    $("#filtros .texto input").each(function() {
        if ($(this).val()!='') {
            data['filtros'].push("&"+$(this).attr('name')+"="+$(this).val());
        }
    });
    //console.log(data['filtros']);
    return data['filtros'];
}

function enviaDados() {
    var situacao = preencheFiltros();
    situacao = situacao.toString();
    situacao = situacao.replace(/,/g,'');

    $('#map').html('');
    //preencheCamposCoordenadas();
    var dados = 'poligono='+$('#poligono').val()+
    '&submitted='+$('#submitted').val()+ situacao; 
    enviaDadosPython(dados);
    $.ajax({                 
        type: 'POST',                                  
        url: 'source.php',                 
        async: true,                 
        data: dados+"&tipoProcessamento=php",                 
        success: function(response) {
            $("#pontos").attr('value',response);
            
            
        }             
    });           
}

