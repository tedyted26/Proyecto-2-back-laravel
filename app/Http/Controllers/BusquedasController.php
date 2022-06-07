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
            return "";
        }
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
       
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
       
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
