<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Busquedas;

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
        $query = Busquedas::select('*')->where("lugar", $textoBuscado)->first();
        
        if(!empty($query)){
            return $query;
        }
        else{
            return response()->json(["Error" => "No hay coincidencias"]);
        }
        /*
        if(!empty($request->input('texto'))){
            $query->where('lugar', '=', $request->input('texto'));
            $out->writeln($query);
        }*/
        return $query;
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
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
