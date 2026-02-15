using System;
using System.Collections.Generic;
using System.Drawing.Drawing2D;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace lab3
{
    public struct MyPen
    {
        public DashStyle PenStyle;
        public int PenWidth;
        public Color PenColor;

        public MyPen(DashStyle style = DashStyle.Solid, int width = 0, Color? color = null)
        {
            PenStyle = style;
            PenWidth = width;
            PenColor = color ?? Color.Black; //если не указан - черный
        }

        public void Set(DashStyle style, int width, Color color)
        {
            PenStyle = style;
            PenWidth = width;
            PenColor = color;
        }

        public System.Drawing.Pen ToPen() //преобразование в системное перо
        {
            System.Drawing.Pen p = new System.Drawing.Pen(PenColor, PenWidth);
            p.DashStyle = PenStyle;
            return p;
        }
    }

    public class CMatrix
    {
        private double[,] data;

        public CMatrix(int rows = 3, int cols = 3)
        {
            data = new double[rows, cols];
        }

        public double this[int r, int c]
        {
            get => data[r, c];
            set => data[r, c] = value;
        }
    }

    public class CPlot2D
    {
        private List<float> X = new List<float>();
        private List<float> Y = new List<float>();
        private CMatrix K = new CMatrix(3, 3);
        private Rectangle RW;
        private RectangleF RS;
        private MyPen PenLine = new MyPen(DashStyle.Solid, 2, Color.Red);
        private MyPen PenAxis = new MyPen(DashStyle.Solid, 1, Color.Black);

        public void SetParams(List<float> xx, List<float> yy, Rectangle rwx, RectangleF fixedRS)
        {
            X = xx;
            Y = yy;
            RW = rwx;
            RS = fixedRS;
            K = SpaceToWindow(RS, RW);
        }

        public bool ShowAxis { get; set; } = false;

        public static CMatrix SpaceToWindow(RectangleF rs, Rectangle rw)
        {
            CMatrix k = new CMatrix(3, 3);

            double sx = (double)rw.Width / (rs.Right - rs.Left); //масштаб по X
            double sy = -(double)rw.Height / (rs.Bottom - rs.Top); //мастштаб по Y
            double tx = rw.Left - sx * rs.Left; //смещение
            double ty = rw.Top - sy * rs.Bottom;

            k[0, 0] = sx; k[0, 1] = 0; k[0, 2] = tx;
            k[1, 0] = 0; k[1, 1] = sy; k[1, 2] = ty;
            k[2, 0] = 0; k[2, 1] = 0; k[2, 2] = 1;

            return k;
        }

        public void SetParams(List<float> xx, List<float> yy, Rectangle rwx)
        {
            X = xx;
            Y = yy;
            RW = rwx;

            if (X.Count == 0 || Y.Count == 0) return;

            //границы данных
            float xmin = X.Min();
            float xmax = X.Max();
            float ymin = Y.Min();
            float ymax = Y.Max();

            //отступы вокруг данных
            float xPadding = (xmax - xmin) * 0.01f;
            float yPadding = Math.Max((ymax - ymin) * 0.1f, 0.1f);

            RS = new RectangleF(
                xmin - xPadding,
                ymin - yPadding,
                (xmax - xmin) + 2 * xPadding,
                (ymax - ymin) + 2 * yPadding
            );

            K = SpaceToWindow(RS, RW);
        }

        public void SetPenLine(MyPen p) => PenLine = p;
        public void SetPenAxis(MyPen p) => PenAxis = p;

        public void GetWindowCoords(double xs, double ys, out int xw, out int yw) //преобразование конкретной точки
        {
            xw = (int)(K[0, 0] * xs + K[0, 1] * ys + K[0, 2]);
            yw = (int)(K[1, 0] * xs + K[1, 1] * ys + K[1, 2]);
        }


        private void DrawAxisTicks(Graphics g, System.Drawing.Pen pen)
        {
            float tickLength = 5f;
            float stepX = 1f;
            float stepY = 1f;

            using (var font = new Font("Arial", 8))
            using (var brush = new SolidBrush(Color.Black))
            {
                for (float x = (float)Math.Ceiling(RS.Left); x <= RS.Right; x += stepX)
                {
                    GetWindowCoords(x, 0, out int xw, out int yw);
                    g.DrawLine(pen, xw, yw - (int)tickLength, xw, yw + (int)tickLength);
                    g.DrawString(x.ToString("0"), font, brush, xw - 8, yw + 8);
                }

                for (float y = (float)Math.Ceiling(RS.Top); y <= RS.Bottom; y += stepY)
                {
                    GetWindowCoords(0, y, out int xw, out int yw);
                    g.DrawLine(pen, xw - (int)tickLength, yw, xw + (int)tickLength, yw);
                    if (Math.Abs(y) > 0.01)
                        g.DrawString(y.ToString("0"), font, brush, xw + 6, yw - 8);
                }
            }
        }


        public void Draw(Graphics g)
        {
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.Clear(Color.White);

            if (X.Count == 0 || Y.Count == 0) return;

            if (ShowAxis)
            {
                using (var penA = PenAxis.ToPen())
                {
                    if (RS.Top <= 0 && RS.Bottom >= 0)
                    {
                        GetWindowCoords(RS.Left, 0, out int x1, out int y1);
                        GetWindowCoords(RS.Right, 0, out int x2, out int y2);
                        g.DrawLine(penA, x1, y1, x2, y2);
                    }

                    if (RS.Left <= 0 && RS.Right >= 0)
                    {
                        GetWindowCoords(0, RS.Top, out int x1, out int y1);
                        GetWindowCoords(0, RS.Bottom, out int x2, out int y2);
                        g.DrawLine(penA, x1, y1, x2, y2);
                    }
                    DrawAxisTicks(g, penA);
                }
            }

            using (var penL = PenLine.ToPen())
            {
                for (int i = 0; i < X.Count - 1; i++)
                {
                    GetWindowCoords(X[i], Y[i], out int x1, out int y1);
                    GetWindowCoords(X[i + 1], Y[i + 1], out int x2, out int y2);

                    g.DrawLine(penL, x1, y1, x2, y2);
                }
            }
        }
        public Rectangle GetRW()
        {
            return RW;
        }

        public RectangleF GetRS()
        {
            return RS;
        }
    }
}
