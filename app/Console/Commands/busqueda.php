<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Busquedas;
use App\Models\Noticias;
use App\Models\Twitter;

class busqueda extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'bbdd:busquedas';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $out = new \Symfony\Component\Console\Output\ConsoleOutput();
        $textoBuscado = "Pontevedra";

        $Busqueda = new Busquedas;
        $Busqueda->lugar = $textoBuscado;
        $Busqueda->visitas_totales = 0;
        $Busqueda->resultado_odio = 0;
        

        $readTweets = exec("python ./python-codes/ASTweets.py ".$textoBuscado);
        $out->writeln($readTweets);
        $json_tweets = json_decode($readTweets);
        $out->writeln("Tweets decodificados correctamente");

        $Tweets = new Twitter;
        $Tweets->total_likes = $json_tweets->totalMg;
        $Tweets->total_retweets = $json_tweets->totalRt;
        $Tweets->numero_tweets = $json_tweets->tweetsAnalizados;
        $Tweets->polaridad = $json_tweets->polaridadMedia;
        $Tweets->subjetividad = $json_tweets->subjetividadMedia;

        $out->writeln("Tweets Bien");
        
        $textoBuscado = preg_replace('/\s+/', '', $textoBuscado);
        $out->writeln($textoBuscado);
        $readNews = exec("python ./python-codes/main_clasificador.py ".$textoBuscado);
        if(!empty($readNews)){
            $out->writeln($readNews);
            $json_news = json_decode($readNews, true);
            $out->writeln(gettype($json_news));
            if($json_news != null){
                $Busqueda->save();
                $id = $Busqueda->id;
                $Tweets->busquedas_id = $id;
                $Tweets->save();

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
                $out->writeln("FINALIZADO CORRECTAMENTE");
            }
        }
        
        return 0;
    }
}
