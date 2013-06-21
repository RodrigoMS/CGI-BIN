#!/bin/bash -x
# O x é para ativar o modo debug no Script. 
  
  echo 'content-type: text/html'
  echo ''
  # O echo aviza o que vem antes como cabeçalho, 
  # no caso ele enviará as tags html ao browser.
  echo
  echo '<html> 
          <head> 
            <meta charset="utf-8">
            <title> Resposta do sistema </title> 
          </head>
          <body>'

            #O valor vindo pelo post é passado para o variável formulário.
            formulario=$(sed -n '1p')

            #A variável destino é atribuida ao primeiro caracter da variável formulario.
            destino=${formulario:0:1}

            #sed - editor de linhas.
            #p - utilizado para todas as ocorrencias.
            #s - substituição de caracteres por outros ou nenhum.
            #Substitui os dados incompatíveis vindos pelo post.
            formulario=$(echo $formulario| sed 's/+/ /g;s/1nome=//;
              s/2nome=//;s/3nome=//;s/4nome=//;s/senha=//; s/novoNome=//
              ;s/novaSenha=//;s/%2F/\//g;s/%C3%A3/ã/g;s/%C3%A9/é/g;
              s/%C3%B3/ó/g;s/%C3%B5/õ/g;s/%C3%A7/ç/g;s/%40/@/g;
              s/%C3%AD/í/g;s/%C3%BA/ú/g;s/%C3%B9/ù/g;s/%24/$/g;s/%25/%/g')

            #Separação dos dados vindos do formulário.
            #Em cada ocorrencia de & contará uma volta no laço.
            export IFS='&'
            i=0
            for words in $formulario; do
              if [[ $i -eq 0 ]]; then
                nome=$words
              elif [[ $i -eq 1 ]]; then
                nome2=$words
              elif [[ $i -eq 2 ]]; then
                nome3=$words
              elif [[ $i -eq 3 ]]; then
                nome4=$words
              fi
              i=$(($i+1))
            done

#------------------------------ Localizar ------------------------------------#

            #Definição do destino para processamento do comando.
            if [[ $destino = '1' ]]; then
              #Verifica se a variável localizado esta vazia.
              #Se encontrou aparecerá no browser.
              if [[ $(locate $nome) ]]; then
                echo '<h1>'$nome' encontrado em:</h1>'
                #Localiza arquivos e pastas.
                echo '<pre>'$(locate $nome)'</pre>'
              else 
                echo '<h1>Arquivo ou diretório não encontrado !</h1>'
            fi
            echo'<a href="/inicio.html">'Voltar'</a>'

#--------------------------- Fim do Localizar ---------------------------------#


#---------------------------- Últimos logins ----------------------------------#
  
            elif [[ $destino = '2' ]]; then
              if [[ ${nome:0:1} = "-" ]]; then
                echo '<h1>Somente é aceito números positivos !</h1>'
              else
                echo '<center><h1>Os últimos '$nome' logins executados são:</h1>'
                echo '<pre>'
                # Informaçãos sobre os ultimos logins.
                echo $(last -$nome)
                echo '</pre></center>'
              fi
    
#-------------------------- Fim do Últimos logins ------------------------------#


#--------------------------- Manual dos comandos -------------------------------#
  
            elif [[ $destino = '3' ]]; then
              if [[ $(man $nome) ]]; then
                echo '<h1>Manual do comando '$nome'.</h1>'
                #Local dos executáveis
                echo '<h3>Aonde encontra-se os executaveis do '$nome'.</h3>'
                whereis $nome
                #Man page (Páginas do manual de comandos)
                echo '<pre>'$(man $nome)
                echo '</pre></font>'
              else
                echo '<h1>Comando não encontrado ou não existente !</h1>'
              fi

#----------------------- Fim do Manual dos comandos ----------------------------#

#--------------------------- Informações gerais --------------------------------#

            #Executa vários comanos com relação em computador
            elif [[ $destino = '4' ]]; then
              echo '<h2>'$(uname -a)'</h2>'
              echo '<pre><h3>Informações sobre os barramentos PCI conectados</h3>'
              lspci
              echo '<h3>Informações sobre os dispositivos USB conectados</h3>'
              lsusb
              echo '<h3>Status dos módulos no Kernel Linux</h3>'
              lsmod
              echo '<h3>Memória RAM</h3>'
              free -b
              echo '<h3>Relatório de estatísticas de memória virtual</h3>'
              vmstat -s
              echo '</pre>'
            fi

#------------------------- Fim das Informações gerais ------------------------------#          
  echo '</body>'
  echo '</html>'
exit