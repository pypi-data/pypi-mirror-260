# VizQ

## Description
Tool to create plots based on CPU, GPU and memory usage.

## Installation
```
pip install vizq
```

## Usage
You can see the options of this project by doing `python -m vizq.visualizaion --help`

```
usage: visualization.py [-h] [-f FILES] [-m MEMORY] [-o OUTPUT] [-c CPU_TIMELINE_TITLE] [-cxl CPU_X_AXIS_LABEL] [-cyl CPU_Y_AXIS_LABEL] [-g GPU_TIMELINE_TITLE]
                        [-gxl GPU_X_AXIS_LABEL] [-gyl GPU_Y_AXIS_LABEL] [-r RSS_TIMELINE_TITLE] [-rxl RSS_X_AXIS_LABEL] [-ryl RSS_Y_AXIS_LABEL] [-of OFFSET]
                        [--x-range X_RANGE X_RANGE] [-mu {kb,mb,gb}]

optional arguments:
  -h, --help            show this help message and exit
  -f FILES, --file FILES
                        File or files to process. Can specify multiple with: "-f file1.log -f file2.log"
  -m MEMORY, --memory MEMORY
                        Total memory size, expected when values are percentages.
  -o OUTPUT, --output OUTPUT
                        Path of output files.
  -c CPU_TIMELINE_TITLE, --cpu-timeline-title CPU_TIMELINE_TITLE
                        CPU timeline title to use in the plot
  -cxl CPU_X_AXIS_LABEL, --cpu-x-axis-label CPU_X_AXIS_LABEL
                        CPU timeline x axis label to use in the plot
  -cyl CPU_Y_AXIS_LABEL, --cpu-y-axis-label CPU_Y_AXIS_LABEL
                        CPU timeline y axis label to use in the plot
  -g GPU_TIMELINE_TITLE, --gpu-timeline-title GPU_TIMELINE_TITLE
                        GPU timeline title to use in the plot
  -gxl GPU_X_AXIS_LABEL, --gpu-x-axis-label GPU_X_AXIS_LABEL
                        GPU timeline x axis label to use in the plot
  -gyl GPU_Y_AXIS_LABEL, --gpu-y-axis-label GPU_Y_AXIS_LABEL
                        GPU timeline y axis label to use in the plot
  -r RSS_TIMELINE_TITLE, --rss-timeline-title RSS_TIMELINE_TITLE
                        RSS timeline title to use in the plot
  -rxl RSS_X_AXIS_LABEL, --rss-x-axis-label RSS_X_AXIS_LABEL
                        RSS timeline x axis label to use in the plot
  -ryl RSS_Y_AXIS_LABEL, --rss-y-axis-label RSS_Y_AXIS_LABEL
                        RSS timeline y axis label to use in the plot
  -of OFFSET, --offset OFFSET
                        Offset line to draw on the chart
  --x-range X_RANGE X_RANGE
                        Start and end of the x axis range to plot
  -mu {kb,mb,gb}, --memory-unit {kb,mb,gb}
                        memory unit to use between [kb, mb, gb]
```

## Examples

Plot specifying chart title and axis titles using a CPU logs.
```
python -m vizq.visualization -f device2/211/cpu_use_20231019-123121.log \
--cpu-timeline-title "CPU Timeline title" \
--cpu-x-axis-label "new X axis label" \
--cpu-y-axis-label "new Y axis label"
```

Plot specifying chart title and axis titles using a GPU logs.

```
python -m vizq.visualization -f device2/211/gpu_20231019-123124.log \
--gpu-timeline-title "GPU Timeline title" \
--gpu-x-axis-label "new X axis label" \
--gpu-y-axis-label "new Y axis label"
```

Plot specifying chart title and axis titles using a rss memory logs.

```
python -m vizq.visualization -f device2/211/rss_mem_20231019-123119.log \
--rss-timeline-title "RSS memory timelie" \
--rss-x-axis-label "new X axis label" \
--rss-y-axis-label "new Y axis label"
```

Use the offset, X axis range and memory unit example.
--offset draws an horizontal line at the specified value, would be a fixed line at offset value, not a percentage.
--x-range will just save the portion of the plot for the range [x1, x2]
--memory-unit could be one of [kb, mb, gb] and will convert the values in the chart to one of those units.
```
python -m vizq.visualization -f device2/211/rss_mem_20231019-123119.log --offset 90 --x-range 50 150 --memory-unit mb
```


## Contributing
Instructions on how to contribute to the project

## References
Link to references used in the project (Books, posts, videos, courses, repos, etc.)
