<img src ="https://portal.ufpel.edu.br/wp-content/themes/Portal/imagens/header.svg">
<h2> Cache Simulator </h2>
<ul>
<li> Trabalho de simulador de caches </li>
<li> Disciplina Arquitetura e Organização de Computadores 2</li>
<li>Desenvolvido por Arthur Souza e Rafael Grimmler</li>
  <li>Funcionamento</li>
  <ul>
<li>
  O simulador recebe como entrada um único comando</li>
    <li>cache_simulator nsets bsize assoc substituição flag_saida arquivo_de_entrada
  </li>
    <li>nsets é o número de índices</li>
    <li>bsize é o tamanho do bloco</li>
    <li>assoc é o número de associatividade</li>
    <li>substituição é a política usada</li>
    <li>flag_saida define o modo de exibição do resultado</li>
    <li>arquivo_de_entrada é o arquivo com binários usados para execução</li>
  </ul>
  <li>Estrutura do programa
  <ul>
    <li>cache_simulator é o nome do programa</li>
    <li>nSets é o número inteiro que representa a quantidade de índices da cache</li>
    <li>nBlockSize é o número inteiro que representa o tamanho do bloco em bytes</li>
    <li>nAssoc é o número inteiro que representa a associatividade da memória</li>
    <li>subs é o char que representa a política de substituição aplicada, podendo ser R para Random, L para Last Recent Used e F para First In First Out</li>
    <li>nFlag é o modo de exibição de informações no término da execução, podendo ser 0 para o formato de matriz e 1 para especificações</li>
    <li>file é o nome com formato do arquivo usado para simular as requisições de endereços</li>
    <li>mem é o array que contem a memória cache</li>
    <li>nAccess é o número de acessos realizados</li>
    <li>nHits é o número de hits</li>
    <li>nMiss é o número de misses</li>
    <li>nMissComp é o número de misses compulsórios</li>
    <li>nMissCap é o número de misses de capacidade</li>
    <li>nMissConf é o número de misses de conflito</li>
    <li>fifoList é um array auxiliar usado para controle de substituição do FIFO</li>
    <li>bloco tem formato dois formatos de lista</li> 
    <ul>
    <li>bit de validade e tag</li>
    <li>bit de validade, tag e índice da política de LRU</li>
    </ul>
    </ul>
  <li>Bibliotecas usadas</li>
    <ul>
    <li>os.path para testar se o arquivo existe</li>
    <li>math para realizar cálculos de endereçamento</li>
    <li>random para operações com a substituição</li>
  </ul>
  <li>Saída</li>
  <ul>
    <li>Flag 0</li>
    <ul>
      <li>estado final da memória</li>
      <li>política de substituição</li>
      <li>número de acessos</li>
      <li>percentual de hits</li>
      <li>percentual de misses</li>
      <li>percentual de misses compulsórios</li>
      <li>percentual de misses de capacidade</li>
      <li>percentual de misses de conflito</li>
    </ul>
    <li>Flag 1</li>
    <ul>
      <li>número de acessos</li>
      <li>Taxa de hit</li>
      <li>Taxa de miss</li>
      <li>Taxa de miss compulsório</li>
      <li>Taxa de miss de capacidade</li>
      <li>Taxa de miss de conflito</li>
    </ul>
  </ul>
</ul>
