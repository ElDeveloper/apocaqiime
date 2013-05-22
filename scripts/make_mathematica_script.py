#!/usr/bin/env python
# File created on 20 May 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from os.path import join
from cogent.util.misc import makedirs
from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-i','--input_dir',type="string", help='the path where the '
    'trajectory files are located'),
    make_option('-o','--output_dir',type="new_dirpath", help='the output '
    'directory'),
    make_option('-n', '--frames',type="int", help='the number of frames that we '
    'want created from the input files'),
    make_option('-s', '--step_size', type="int", help='number of frames per '
    'script  i. e. the number of images each script will create')
]
script_info['optional_options'] = [
    make_option('-q', '--qsub_calls_filepath', type="new_filepath", help='path '
    'to write the PBS command calls [default: %default]', default=None)
]
script_info['version'] = __version__



def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    frames = opts.frames
    step_size = opts.step_size
    output_path = opts.output_dir
    input_dir = opts.input_dir
    qsub_calls_filepath = opts.qsub_calls_filepath

    try:
        makedirs(output_path)
    except:
        pass

    for i in range(0,int(frames/(step_size*1.0))):
        lower_bound = int((step_size*i)+1)
        upper_bound = int(step_size*i+step_size)

        filename = 'mathematica_script_%d_%d.m' % (lower_bound, upper_bound)
        script_filename = join(output_path, filename)


        fd = open(script_filename, 'w') 
        fd.write(MATHEMATICA_SCRIPT % (frames, input_dir+'/', lower_bound, upper_bound))
        fd.close

        if qsub_calls_filepath:
            fd = open(qsub_calls_filepath, 'a')
            fd.write(QSUB_STRING_CMD % (filename, 'MMA_%d_%d' % (lower_bound,
                upper_bound)))
            fd.close()


QSUB_STRING_CMD = """\
echo "math -script ${PWD}/%s" | qsub -N %s -l mem=16gb -q short -X -V -I
"""

MATHEMATICA_SCRIPT = """
DictHasKey = Function[{dict, key}, ValueQ[dict[key]]];

DictAddKey = 
  Function[{dict, key, value}, 
   If[DictHasKey[dict, key], 
    Print["Warning, Dictionary already has key " <> ToString[key]]];
   dict[key] = value;];

DictKeys = Function[{dict}, res = {};
   ForEach[DownValues[dict], 
    Function[{dictKeyDescr}, 
     res = Append[
        res, ((dictKeyDescr[[1]]) /. 
           dict -> neverUsedSymbolWhatever)[[1, 1]]];]];
   res];

DictValues = Function[{dict}, res = {};
   ForEach[DownValues[dict], 
    Function[{dictKeyDescr}, res = Append[res, dictKeyDescr[[2]]];]];
   res];

DictKeyValuePairs = Function[{dict}, res = {};
   ForEach[DownValues[dict], 
    Function[{dictKeyDescr}, 
     res = Append[
        res, {((dictKeyDescr[[1]]) /. 
            dict -> neverUsedSymbolWhatever)[[1, 1]], 
         dictKeyDescr[[2]]}];]];
   res];

ForEach = Function[{list, func}, len = Length[list];
   For[i = 1, i <= len, i++, func[list[[i]]];];];

  QIIMEColors = {Red, Blue, Orange, Pink, Purple, Yellow, Cyan, Brown, 
   Gray, Magenta, Green, LightRed, LightGreen, LightBlue, LightGray, 
   LightCyan, LightMagenta};
FramesPerStep = %d;

InputPath = "%s";

SetDirectory[InputPath];
ColorByFileNames = FileNames["color_by_*.txt"];

Print["generating the legend file ..."]

Export[InputPath <> "legends.png", 
  Table[Style[ToString[ColorByFileNames[[index]] <> "\n"], 
     QIIMEColors[[index]], "Title"], {index, 1, Length[ColorByFileNames], 1}] // TableForm];

viewpoints = {{-0.9392689875387656`, -0.17156178582741832`, 
    3.246280998726329`}, {-3.0127182859826553`, -0.9075080380805878`, 
    1.2449729676281545`}, {0.07004685347986293`, \
-0.6526469849689273`, -3.319509805879256`}, {2.9383831520771797`, 
    1.5367852258052257`, -0.6739403692729474`}, {1.219046512965905`, 
    1.8953431594792718`, 
    2.524202826050394`}, {-0.9392689875387656`, -0.17156178582741832`,
     3.246280998726329`}, {-0.9392689875387656`, \
-0.17156178582741832`, 3.246280998726329`}};
xViewPointFunction = 
  Interpolation[viewpoints[[1 ;; Length[viewpoints], 1]], 
   InterpolationOrder -> 1];
yViewPointFunction = 
  Interpolation[viewpoints[[1 ;; Length[viewpoints], 2]], 
   InterpolationOrder -> 1];
zViewPointFunction = 
  Interpolation[viewpoints[[1 ;; Length[viewpoints], 3]], 
   InterpolationOrder -> 1];
xviewPoints = 
  Table[xViewPointFunction[h], {h, 1, 
    Length[viewpoints], (Length[viewpoints] - 1)/(10*
       FramesPerStep)}];
yviewPoints = 
  Table[yViewPointFunction[h], {h, 1, 
    Length[viewpoints], (Length[viewpoints] - 1)/(10*
       FramesPerStep)}];
zviewPoints = 
  Table[zViewPointFunction[h], {h, 1, 
    Length[viewpoints], (Length[viewpoints] - 1)/(10*FramesPerStep)}];


verticalpoints = {{-0.3745304696346006`, 0.863381368979908`, 
    0.6801729362437343`}, {-0.821376653461546`, 0.6567945407522666`, 
    0.04206857125820857`}, {-0.33578138983561573`, 
    0.6904999719495469`, -0.9038747251036048`}, {0.1149013895786227`, 
    1.080604755506752`, -0.4107534995687655`}, {-0.10702668164961196`,
     1.140924023975901`, 0.1259613708739166`}, {-0.3745304696346006`, 
    0.863381368979908`, 0.6801729362437343`}, {-0.3745304696346006`, 
    0.863381368979908`, 0.6801729362437343`}};
xViewPointFunction = 
  Interpolation[verticalpoints[[1 ;; Length[verticalpoints], 1]], 
   InterpolationOrder -> 1];
yViewPointFunction = 
  Interpolation[verticalpoints[[1 ;; Length[verticalpoints], 2]], 
   InterpolationOrder -> 1];
zViewPointFunction = 
  Interpolation[verticalpoints[[1 ;; Length[verticalpoints], 3]], 
   InterpolationOrder -> 1];
xverticalPoints = 
  Table[xViewPointFunction[h], {h, 1, 
    Length[verticalpoints], (Length[viewpoints] - 1)/(10*
       FramesPerStep)}];
yverticalPoints = 
  Table[yViewPointFunction[h], {h, 1, 
    Length[verticalpoints], (Length[viewpoints] - 1)/(10*
       FramesPerStep)}];
zverticalPoints = 
  Table[zViewPointFunction[h], {h, 1, 
    Length[verticalpoints], (Length[viewpoints] - 1)/(10*
       FramesPerStep)}];

For[index = 1, index <= Length[ColorByFileNames], index++,
  FileDictionary[ColorByFileNames[[index]]] = 
   ReadList[ColorByFileNames[[index]]]
  ];

Print["loading the data ..."]
Clear[Results, OriginalData];
For[index = 1, index <= Length[DictKeyValuePairs[FileDictionary]], 
  index++,
  (*the second element of these lists is a list of trajectory file \
prefixes*)
  
  CategoryName = DictKeyValuePairs[FileDictionary][[index, 1]];
  FileNamesList = DictKeyValuePairs[FileDictionary][[index, 2]];
  BUFFER = {};
  OBUFFER = {};
  
  For[subIndex = 1, subIndex <= Length[FileNamesList], subIndex++,
   
   If[FileExistsQ[ToString[FileNamesList[[subIndex]]] <> ".txt"] == 
     False, Continue[]];
   
   (*remember to cast to strings the keys, 
   as they by default are not strings *)
   
   subjectData = 
    ReadList[
     ToString[FileNamesList[[subIndex]]] <> ".txt", {Number, Number, 
      Number}];
   (*Print["The length of subject "<>ToString[FileNamesList[[
   subIndex]]]<>" "<>ToString[Length[subjectData]]]*)
   
   xSubjectFunction = 
    Interpolation[subjectData[[1 ;; Length[subjectData], 1]], 
     InterpolationOrder -> 1];
   ySubjectFunction = 
    Interpolation[subjectData[[1 ;; Length[subjectData], 2]], 
     InterpolationOrder -> 1];
   zSubjectFunction = 
    Interpolation[subjectData[[1 ;; Length[subjectData], 3]], 
     InterpolationOrder -> 1];
   
   (*create the tables of points*)
   
   dataPoints = 
    Table[{xSubjectFunction[h], ySubjectFunction[h], 
      zSubjectFunction[h]}, {h, 1, Length[subjectData], 
      N[1/FramesPerStep]}];
   BUFFER = Append[BUFFER, dataPoints];
   OBUFFER = Append[OBUFFER, subjectData];
   (*Print["The number of data points is: "<>ToString[Length[
   dataPoints]]]*)
   ];
  Results[ToString[CategoryName]] = BUFFER;
  OriginalData[ToString[CategoryName]] = OBUFFER;
  ];

DataForCategories = DictKeyValuePairs[Results];
OriginalDataForCategories = DictKeyValuePairs[OriginalData];
Print["generating the frames ..."]

theframes = Table[
   Show[
    ArrayFlatten[
     Table[
      Table[
       
       (*Not all the trajectorys have the same number of points, 
       so check if the current frame requres more or not*)
       
       actualFrame = 
        If[frame > 
          Length[DataForCategories[[category, 2, trajectory]]], 
         Length[DataForCategories[[category, 2, trajectory]]], 
         frame];
       
       tubePoints = If[actualFrame > FramesPerStep
         ,
         Join[
          
          OriginalDataForCategories[[category, 2, trajectory, 
           1 ;; Floor[actualFrame/FramesPerStep]]],
          
          DataForCategories[[category, 2, trajectory, 
           Floor[(actualFrame/FramesPerStep)]*FramesPerStep ;; 
            actualFrame]]
          ]
         ,
         DataForCategories[[category, 2, trajectory, 
          1 ;; actualFrame]]];
       
       Graphics3D[
        {QIIMEColors[[category]],
         (*Thickness[0.5],*)
         Opacity[0.4],
         Tube[tubePoints, 0.0010]
         }
        (*Graphics 3D call*)
        ]
       , {trajectory, 1, Length[DataForCategories[[category, 2]]] - 1,
         1}]
      
      , {category, 1, Length[DataForCategories], 1}]
     
     (* Flattening the table*)
     , 1]
    
    (*Showing all elements of the array*)
    , Background -> White,
    Boxed -> False,
    BoxRatios -> Automatic,
    ViewPoint -> {xviewPoints[[frame]], yviewPoints[[frame]], 
      zviewPoints[[frame]]},
    ViewVertical -> {xverticalPoints[[frame]], 
      yverticalPoints[[frame]], zverticalPoints[[frame]]},
    (*ViewPoint\[Rule]{xviewPoints[[frame]],yviewPoints[[frame]],
    zviewPoints[[frame]]},*)(*{-0.7141497385420787`,
    1.1428379236298871`,
    3.103854318626056`},*)
    (*ViewVertical\[Rule]{xverticalPoints[[
    frame]],yverticalPoints[[frame]],zverticalPoints[[
    frame]]},*)(*{-0.12288126982496617`,1.0964096362645268`,
    0.350234163260499`},*)
    RotationAction -> "Clip",
    ImageSize -> {960*2, 540*2}
    ]
   
   (*Animate specific settings*)
   , {frame, 1, 10*FramesPerStep, 1}(*,
   DisplayAllSteps\[Rule]True,AnimationRepetitions\[Rule]1,
   AnimationRunning \[Rule] False*)
   ];
Print["Frames generated ... time to export"]

For[j=%d,j<=%d,j++,


Print["About to export frame "<>ToString[j]<>"..."]
Export[InputPath<>ToString[j]<>".png", theframes[[j]]]
Print["Frame "<>ToString[j]<>" exported ..."]
]
Print["All frames have been created"]
"""


if __name__ == "__main__":
    main()