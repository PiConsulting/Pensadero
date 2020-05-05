# Funcion GetDayName
#
## Objetivo

Esta función personalizada lo que va a devolver es el nombre del dia de la fecha solicitada en el idioma de tu preferencia utilizando la función **Date.DayOfWeekName** en Power Query agregando un parámetro poco usado en las funciones del tipo Fecha, el parámetro 'culture'.

Nuestra funcion *GetDayName* recibe 2 parametros, *GetDayName(mydate as date, language as text)*

  - El parámetro *mydate* es la fecha que se va a usar para extraer el Nombre del dia.
  - El párametro *language* es el idioma en que queremos obtener el Nombre del dia.

Lamentablemente a la funcion **Date.DayName** no recibe nativamente el idioma en que queremos el resultado, sino el parámetro 'culture' el cual es el locale (adaptacion cultural) que se va a aplicar a la función.

Los locales mas conocidos son **es** para español y **en** para ingles.

Nuestra funcion va a recibir el parametro language (Spanish, English, Chinese, German, Italian, etc..) y solo tenemos que buscar una fuente que tenga el codigo locale para el idioma que especifiquemos.

## Preparación

En este caso hacemos uso de una pagina en Wikipedia [WikipediaLanguageLocalisation]:

[![N|Solid](https://gdurl.com/wu0Z)](https://gdurl.com/wu0Z)

Nos conectamos a esta pagina de Wikipedia mediante el conector web en Power Query y luego de aplicar unos simples pasos en Power Query nos quedamos con la informacion que necesitamos:

[![N|Solid](https://gdurl.com/cLKJ)](https://gdurl.com/cLKJ)

De esta manera, esta tabla nos va a servir para que que busquemos el locale necesario para el idioma que queramos usar.
Luego de agregar una columna adicional y un filtro, procedemos a convertir el query en una funcion y ya podemos usarlo.

## Código

Para crear ésta función, solo crea un Query en blanco con un nombre de tu preferencia en tu Power Query Editor, abre el Editor Avanzado, si hubiera algun codigo dentro borra todo y pega el siguiente código:

```
(mydate as date, language as text)=>
let
    Source = Web.BrowserContents("https://en.wikipedia.org/wiki/Language_localisation"),
    SourceTable = Html.Table(Source, {{"Column1", "TABLE.wikitable > * > TR > TH:not([colspan]):not([rowspan]):nth-child(1):nth-last-child(3), TABLE.wikitable > * > TR > TD[rowspan=""6""]:not([colspan]):nth-child(1):nth-last-child(3), TABLE.wikitable > * > TR > TD[rowspan=""2""]:not([colspan]):nth-child(1):nth-last-child(3), TABLE.wikitable > * > TR > TD[rowspan=""3""]:not([colspan]):nth-child(1):nth-last-child(3), TABLE.wikitable > * > TR > TD[rowspan=""7""]:not([colspan]):nth-child(1):nth-last-child(3), TABLE.wikitable > * > TR > TD[rowspan=""5""]:not([colspan]):nth-child(1):nth-last-child(3), TABLE.wikitable > * > TR > TD[rowspan=""4""]:not([colspan]):nth-child(1):nth-last-child(3), TABLE.wikitable > * > TR > TD[rowspan=""8""]:not([colspan]):nth-child(1):nth-last-child(3)"}, {"Column2", "TABLE.wikitable > * > TR > TH:not([colspan]):not([rowspan]):nth-child(1):nth-last-child(3) + TH:not([colspan]):not([rowspan]):nth-child(2):nth-last-child(2), TABLE.wikitable > * > TR > TD[rowspan=""6""]:not([colspan]):nth-child(1):nth-last-child(3) + TD:not([colspan]):not([rowspan]):nth-child(2):nth-last-child(2), TABLE.wikitable > * > TR > TD:not([colspan]):not([rowspan]):nth-child(1):nth-last-child(2), TABLE.wikitable > * > TR > TD[rowspan=""2""]:not([colspan]):nth-child(1):nth-last-child(3) + TD:not([colspan]):not([rowspan]):nth-child(2):nth-last-child(2), TABLE.wikitable > * > TR > TD[rowspan=""3""]:not([colspan]):nth-child(1):nth-last-child(3) + TD:not([colspan]):not([rowspan]):nth-child(2):nth-last-child(2), TABLE.wikitable > * > TR > TD[rowspan=""7""]:not([colspan]):nth-child(1):nth-last-child(3) + TD:not([colspan]):not([rowspan]):nth-child(2):nth-last-child(2), TABLE.wikitable > * > TR > TD[rowspan=""5""]:not([colspan]):nth-child(1):nth-last-child(3) + TD:not([colspan]):not([rowspan]):nth-child(2):nth-last-child(2), TABLE.wikitable > * > TR > TD[rowspan=""4""]:not([colspan]):nth-child(1):nth-last-child(3) + TD:not([colspan]):not([rowspan]):nth-child(2):nth-last-child(2), TABLE.wikitable > * > TR > TD[rowspan=""8""]:not([colspan]):nth-child(1):nth-last-child(3) + TD:not([colspan]):not([rowspan]):nth-child(2):nth-last-child(2)"}}, [RowSelector="TABLE.wikitable > * > TR"]),
    SplitCode = Table.SplitColumn(SourceTable, "Column2", Splitter.SplitTextByDelimiter("-", QuoteStyle.Csv), {"Column2.1", "Column2.2"}),
    ChangeType = Table.TransformColumnTypes(SplitCode,{{"Column2.1", type text}, {"Column2.2", type text}}),
    SelectColumns = Table.SelectColumns(ChangeType,{"Column1", "Column2.1"}),
    PromoteHeader = Table.PromoteHeaders(SelectColumns, [PromoteAllScalars=true]),
    RemoveNull = Table.SelectRows(PromoteHeader, each ([Language family] <> null)),
    AddDayNameColumn= Table.AddColumn(RemoveNull, "DayName", each Date.DayOfWeekName(mydate, [Language tag])),
    SelectLanguage = Table.SelectRows(AddDayNameColumn, each (Text.Lower([Language family]) = Text.Lower(language))),
    Result = Text.Proper(SelectLanguage{0}[DayName])
in
    Result
```

** Si se percatan, desde el paso *SourceTable* hasta el paso *SplitCode* son lineas autogeneradas por el conector web de Power Query a la hora de escoger la tabla de la pagina de Wikipedia.

## Uso

Para comenzar a usar esta funcion, solo te ubicas en la tabla donde tengas tu fecha, agregas una columna personalizada e invocas a la función que acabamos de crear (en mi caso *GetDayName*) indicandole el campo donde esta tu fecha y escribiendo el idioma en que quieres visualizar el Nombre del Dia:

[![N|Solid](https://gdurl.com/PhAU)](https://gdurl.com/PhAU)

En nuestra función el parametro de idioma *language* lo hicimos **Case Insensitive**, por lo que no tenemos que preocuparnos si hay letras mayusculas o minusculas al escribirlo.

Podemos aplicarlo utilizando el idioma que necesitemos, al final nos va a mostrar el nombre del dia en el idioma elegido:

[![N|Solid](https://gdurl.com/vfiK)](https://gdurl.com/vfiK)

Y Pum! tenemos los nombres de dias generados automáticamente de cualquier campo fecha en el idioma que se necesite.
#
#
[![N|Solid](https://gdurl.com/litC)](https://gdurl.com/litC)

[//]: # 
   [WikipediaLanguageLocalisation]: <https://en.wikipedia.org/wiki/Language_localisation>