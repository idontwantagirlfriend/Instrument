## Version 0
大家好，我自制了一个分词脚本，能够进行段落、句子和词等级的分割，输出结果按课程要求的标记格式设计，且可以直接复制到excel中（没进行L2-L6的标记，有句子序号）。届时只需要在L2-L6行进行标记。会使用python的同学或许可以省下一点点时间。
使用方法：
1. 在文本文件目录下运行。
2. 输入文本文件路径(path)和输出文件路径(export)到main(path,export)方法。
3. 复制输出文件(export)的内容，在excel中直接粘贴。
设计时针对使用空格且引号形式为半角双引号""或 « »的语言（包括非拉丁字母的语言）。

A word level segmentation tool that is made for Leipzig interlinear translation. The output content is formatted for direct copypaste to excel .xlsx files.
**Still command level user interface, but fair enough**
1.  Paste "paraseg.py" to the directory of raw texts;
2.  Launch the method with the following parameters: [paraseg.]main(path,export);
2.1.  path: path of the raw texts to process;
2.2.  export: target path for the glossed texts;
3.  Find the glossed texts at the location given at (export) parameter, and paste the content directly into an excel sheet.

## Version 1.0
**Attention** This program is for program assisted *Leipzig interlinear glossing*. Currently, the morpheme-by-morpheme glossing is supported only for the following language combination: {(L1:fr)(L2:seg_fr)(L3:en)(L4)(L5:zh)(L6)}. 
Updated pool_zh, pool_en, pool_seg to enable program assisted glossing. Use seg.py to match tokens with glossing contents. Added word count indicator and automatic glossing percentage indicator. 
Word level segmentation is done directly in paraseg and is operational for alphabetical languages that uses upper flat double quotation marks (""), opening and closing double quotation marks (“”), and French left and right quotation marks "«»".
## Version 1.1
Revised indicator: .2% format.
## Version 1.1.2 
Removed deprecated methods. Added launcher. 
