from grsh_data_api.util import Tool
from grsh_data_api._mychart.base import Chart, GMPL, mpl, plt


class GmplEmpty(GMPL):
    def plot(self):
        try:
            with self._lock:
                plt.close("all")
                _, ax = plt.subplots()
                ax.plot()
                ax.axis("off")
                param = self.element.param
                if param and 'background_str' in param:
                    text = param['background_str']
                else:
                    text = 'T O D O'
                ax.text(0.5, 0.5, text,
                        transform=ax.transAxes,
                        fontsize=50, color='gray',
                        alpha=0.1,
                        ha='center',
                        va='center',
                        rotation=30
                        )
            self._save_base64()
        except Exception as e:
            raise e
        finally:
            pass

class ChartEmpty(Chart):
    name = "empty"
    desc = "空白图片"
    num = "0"
    gmpl_class = GmplEmpty

    def prepare_data(self):
        pass
