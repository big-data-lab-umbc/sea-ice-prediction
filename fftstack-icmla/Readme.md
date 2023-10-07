# Integrating Fourier Transform and Residual Learning for Arctic Sea Ice Forecasting

## Abstract
Arctic sea ice plays integral roles in both polar and global environmental systems, notably ecosystems, communities, and economies. As sea ice continues to decline due to climate change, it has become imperative to accurately predict the future of sea ice extent (SIE). Using datasets of Arctic meteorological and SIE variables spanning 1979 to 2021, we propose architectures capable of processing multivariate time series and spatiotemporal data. Our proposed framework consists of ensembled stacked Fourier Transform signals (FFTstack) and Gradient Boosting models. In FFTstack, grid search iteratively detects the optimal combination of representative FFT signals, a process that improves upon current FFT implementations and deseasonalizers. An optimized Gradient Boosting Regressor is then trained on the residual of the FFTstack output. Through experiment, we found that the models trained on both multivariate and spatiotemporal time series data performed either similar to or better than models in existing research. In addition, we found that integration of FFTstack improves the performance of current multivariate time series deep learning models. We conclude that the high flexibility and performance of this methodology have promising applications in guiding future adaptation, resilience, and mitigation efforts in response to Arctic sea ice retreat.

## Paper
The paper has been accepted in the proceedings of IEEE ICMLA 2023. A copy of pre-print can be provided upon request.

## Code
1. Install required dependencies with `%pip install -r requirements.txt`
2. Navigate repository by model type:

| Folder | Description |
| - | - |
| multivariate | Load/process multivariate data, train multivariate models |
| spatiotemporal | Load/process spatiotemporal data, train spatiotemporal model |
| transformers | Contains FFTStack and conditional linear detrending code for use by above models |

**Note:** The file structure is not static; new folders/files may be generated as code is run.  


## Citation
If you use this code for your research, please cite our paper:
`Pending update`
