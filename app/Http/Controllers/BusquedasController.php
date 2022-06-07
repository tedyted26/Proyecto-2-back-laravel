<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\Http\Request;
use App\Models\Busquedas;
use App\Models\Noticias;
use App\Models\Twitter;

class BusquedasController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return Busquedas::orderBy('created_at', 'asc')->get();
    }

    /**
     * Dado un texto, devuelve la busqueda encontrada
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function getSearch(Request $request){
        $out = new \Symfony\Component\Console\Output\ConsoleOutput();
        $textoBuscado = $request->input('texto');

        $busqueda_q = Busquedas::select('*')->where("lugar", $textoBuscado)->first();

        if(!empty($busqueda_q)){
            $id_busqueda = $busqueda_q->id;
            $out->writeln($id_busqueda);
            $suma = $busqueda_q->visitas_totales + 1;
            $busqueda_q->visitas_totales = $suma;
            $busqueda_q->save();

            $noticias_json = Noticias::select('id','url', 'titulo', 'subtitulo',
             'resultado','fecha_noticia')
            ->where("busquedas_id", $id_busqueda)->get();

            $tweets_q = Twitter::select('id','numero_tweets', 'polaridad', 'subjetividad')
           ->where("busquedas_id", $id_busqueda)->first();
           
            $compound_json = json_encode(array("noticias" =>  $noticias_json, "twitter" => $tweets_q));

            return $compound_json;
        }
        else{
            $out->writeln("Provincia no encontrada en BBDD");
            
            $Busqueda = new Busquedas;
            $Busqueda->lugar = $textoBuscado;
            $Busqueda->visitas_totales = 0;
            $Busqueda->resultado_odio = 0;
            $Busqueda->save();
            $id = $Busqueda->id;

            $readTweets = exec("python ./python-codes/ASTweets.py ".$textoBuscado);
            $out->writeln($readTweets);
            $json_tweets = json_decode($readTweets);

            $Tweets = new Twitter;
            $Tweets->total_likes = $json_tweets->totalMg;
            $Tweets->total_retweets = $json_tweets->totalRt;
            $Tweets->numero_tweets = $json_tweets->tweetsAnalizados;
            $Tweets->polaridad = $json_tweets->polaridadMedia;
            $Tweets->subjetividad = $json_tweets->subjetividadMedia;
            $Tweets->busquedas_id = $id;
            $Tweets->save();
            $out->writeln("Tweets Bien");
            
            $textoBuscado = preg_replace('/\s+/', '', $textoBuscado);

            $readNews = exec("python ./python-codes/main_clasificador.py ".$textoBuscado);
            $out->writeln($readNews);
            $json_news = json_decode($readNews, true);

            foreach ($json_news as &$noticia) {
                $Noticia = new Noticias;
                $Noticia->url = $noticia["url"];
                $Noticia->titulo = $noticia["titulo"];
                $Noticia->subtitulo = $noticia["subtitulo"];
                $Noticia->resultado = $noticia["resultados"];
                $Noticia->fecha_noticia = "2022-01-01";
                $Noticia->busquedas_id = $id;
                $Noticia->save();
            }
            
            /*

            foreach ($json_news as &$noticia) { 
                $Noticia = new Noticias;
                $Noticia->url = $noticia["url"];
                $out->writeln($noticia["url"]);
                $Noticia->titulo = $noticia["titulo"];
                $out->writeln($noticia["titulo"]);
                $Noticia->subtitulo = $noticia["subtitulo"];
                $out->writeln($noticia["subtitulo"]);
                $Noticia->fecha = "2022-01-01";
                $out->writeln($Noticia->fecha);
                $Noticia->resultado = $noticia["resultados"];
                $out->writeln($noticia["resultados"]);
                $Noticia->busquedas_id = 1;
                $out->writeln($Noticia->busquedas_id);
                $Noticia->save();
                $out->writeln("TODO BIEN");
            }
            */
            
            

            /*
            error_reporting(E_ALL);
            ini_set('display_errors', 1);
            $readTweets = exec("python ./python-codes/ASTweets.py ".$textoBuscado);
            $readNews = exec("python ./python-codes/main_clasificador.py ".$textoBuscado);
            */
            /*
            $readNewsText = "[{url: https://www.abc.es/historia/abci-grandiosa-iglesia-y-hospital-contra-peste-presidio-puerta-durante-500-anos-202010050116_noticia.html,titulo: La grandiosa iglesia y hospital contra la peste que presidi la Puerta del Sol durante 500 aos,subtitulo: Las obras de la estacin de Cercanas de la cntrica plaza madrilea sacaron a la luz los restos de la cimentacin del antiguo templo del Buen Suceso, construido en el siglo XV. Y all estuvo durante varios siglos sufriendo reformas y guerras como de la Independencia contra los franceses, hasta que tuvo que ser demolida en 1854 ,fecha_noticia: 2022-05-27T17:24:38Z,resultados: -1},{url: https://www.abc.es/historia/abci-misterios-historia-egipcios-dejaron-construir-piramides-201902240207_noticia.html,titulo: Misterios de la Historia: Por qu los egipcios dejaron de construir pirmides?,subtitulo: Con la III Dinasta aprendieran a hacer pirmides, con la IV alcanzaron la excelencia en Giza y Dasur y con la V parecieron olvidar cmo se construan con las perfectas caractersticas de sus predecesores. No obstante, hasta el Imperio Nuevo se siguieron levantando algunas, aunque sus materiales eran peores y no han podido pervivir hasta la actualidad,fecha_noticia: 2022-05-27T16:59:08Z,resultados: -1},{url: https://www.abc.es/deportes/abci-cuba-no-frena-estampida-otro-atleta-escapa-nada-mas-pisar-aeropuerto-barajas-202205261028_noticia.html,titulo: Cuba no frena la estampida: otro atleta se escapa nada ms pisar el aeropuerto Barajas,subtitulo: Jenns Fernndez, 'la centella de Simpson', el gran talento de la velocidad de 
                su pas, abandona su seleccin al llegar a  Espaa ,fecha_noticia: 2022-05-26T09:09:27Z,resultados: -1},{url: https://www.abc.es/espana/madrid/abci-linea-8-metro-reabre-este-sabado-tres-dias-antes-previsto-tras-finalizar-obras-202205241154_noticia.html,titulo: La lnea 8 de Metro reabre este sbado, tres das antes de lo previsto, tras finalizar sus obras,subtitulo: 
                Los trabajos afectaban al tramo entre Colombia y Mar de Cristal, pero slo estaba cortada la estacin de Pinar del Rey,fecha_noticia: 2022-05-26T09:25:31Z,resultados: 1},{url: https://www.abc.es/economia/abci-amenaza-huelga-ryanair-sindicatos-barajan-paros-europeos-justo-antes-agosto-202205231917_noticia.html,titulo: Amenaza de huelga en Ryanair: los sindicatos barajan paros europeos justo antes de agosto,subtitulo: Los tripulantes de cabina espaoles piden mejoras salariales a la empresa en el nuevo convenio ,fecha_noticia: 2022-05-24T17:33:57Z,resultados: 1},{url: https://www.abc.es/deportes/abci-juan-espino-encara-nueva-etapa-sandford-gustaria-pelear-septiembre-octubre-202205251021_noticia.html,titulo: Juan Espino encara una nueva etapa en el Sandford MMA: Me gustara pelear en septiembre u octubre,subtitulo: El luchador grancanario se 
                recupera de una operacin en sus codos con optimismo. El desembarco que prepara UFC en Pars es una fecha que baraja para su regreso. Augusto Sakai sera un rival a tener en cuenta,fecha_noticia: 2022-05-25T08:21:38Z,resultados: -1},{url: https://www.abc.es/cultura/musica/abci-misteriosa-semana-espanola-rolling-stones-202205261740_noticia.html,titulo: La misteriosa semana espaola de los Rolling Stones,subtitulo: La banda britnica ha sorprendido a todos aterrizando en Madrid seis das antes de su concierto en el Wanda Metropolitano,fecha_noticia: 2022-05-27T12:09:01Z,resultados: -1},{url: https://www.abc.es/espana/casa-real/abci-juan-carlos-baraja-visitar-espana-proximo-semana-202205161127_noticia.html,titulo: Juan Carlos I baraja visitar Espaa el prximo fin de semana,subtitulo: Los periodistas Carlos Herrera y Fernando nega han desvelado este lunes los planes del padre del Rey,fecha_noticia: 2022-05-17T09:21:19Z,resultados: -1},{url: https://www.abc.es/historia/abci-infierno-division-azul-campos-concentracion-sovieticos-durante-segunda-guerra-mundial-202012130049_noticia.html,titulo: De Mosc a Odessa: el martirio de la Divisin Azul en los campos de concentracin de Stalin,subtitulo: Morir en el campo de batalla no era el peor destino para los divisionarios espaoles; muchos acabaron sus das en las temibles prisiones soviticas, aunque, en la actualidad, se desconoce el nmero exacto,fecha_noticia: 2022-05-27T10:10:00Z,resultados: 1},{url: https://www.abc.es/play/television/eurovision/abci-chanel-bano-masas-llegada-espana-202205152038_noticia.html,titulo: 
                Chanel se da un bao de masas en su llegada a Espaa,subtitulo: La artista ofrece un concierto en la Plaza Mayor, que se puede ver en RTVE Play,fecha_noticia: 2022-05-15T19:37:58Z,resultados: -1}]";
            */
            #$busqueda = {"lugar":"Pamplona","fecha_busqueda":"2022-04-04","visitas_totales":11,"resultado_odio":3.1};
            /*
            $out->writeln($busqueda);
            $busqueda->lugar = "Pamplona";
            $busqueda->fecha_busqueda = "2022-04-04";
            $busqueda->visitas_totales = 11;
            $busqueda->resultado_odio = 3.1;
            $out->writeln($busqueda);
            */
            #$busqueda->save();

            #$out->writeln($busqueda);
            /*
            $busqueda = Busquedas::create([
                'lugar' => 'Pamplona',
                'fecha_busqueda' => '2022-04-04',
                'visitas_totales' => 11,
                'resultado_odio' => 3.1,
            ]);*/
            #$this->store($request);
            /*
            $array = array("Tweets"=>$readTweets, "News"=>$readNews);
            $out->writeln($array);
            $compound_json = json_encode($array);
            $out->writeln($compound_json);
            $out->writeln(gettype($compound_json));
            return $compound_json;
            */
            return "";
        }
        /*
        if(!empty($request->input('texto'))){
            $query->where('lugar', '=', $request->input('texto'));
            $out->writeln($query);
        }*/
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
        /*
        $busqueda = new Busquedas;
        $busqueda->save();
        /*
        $busqueda->lugar = "Pamplona";
        $busqueda->fecha_busqueda = "2022-04-04";
        $busqueda->visitas_totales = 11;
        $busqueda->resultado_odio = 3.1;
        $out->writeln($busqueda);
        $busqueda->save();
        */
        #$out->writeln("todo bIennnnnnnns");
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
        
        $out->writeln("STORE");
        /*
        $out->writeln($request);
        */

    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        return Busquedas::findorFail($id);
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
    }
}
