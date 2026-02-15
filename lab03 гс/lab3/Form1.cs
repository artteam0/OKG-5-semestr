using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace lab3
{
    public partial class Form1 : Form
    {
        private string F = "None";

        public Form1()
        {
            InitializeComponent();

            panel1.Dock = DockStyle.Fill;
            this.DoubleBuffered = true;

            menuStrip1.Items[0].Click += F1;
            menuStrip1.Items[1].Click += F2;
            menuStrip1.Items[2].Click += F3;
            panel1.Paint += panel1_Paint;
            this.Resize += (s, e) => panel1.Invalidate();
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {
            e.Graphics.Clear(Color.White);
            if (F == "None") return;

            List<float> x = new List<float>();
            List<float> y = new List<float>();
            CPlot2D plot = new CPlot2D();

            switch (F)
            {
                case "F1":
                    {
                        for (float i = -3 * (float)Math.PI; i <= 3 * (float)Math.PI; i += (float)Math.PI / 36)
                        {
                            if (Math.Abs(i) < 0.001f) continue;
                            x.Add(i);
                            y.Add(MyF1(i));
                        }
                        plot.ShowAxis = true;
                        plot.SetParams(x, y, panel1.ClientRectangle);
                        plot.SetPenLine(new MyPen(DashStyle.Solid, 1, Color.Red));
                        plot.SetPenAxis(new MyPen(DashStyle.Solid, 2, Color.Blue));
                        plot.Draw(e.Graphics);
                        break;
                    }
                case "F2":
                    {
                        for (float i = -4 * (float)Math.PI; i <= 4 * (float)Math.PI; i += (float)Math.PI / 36)
                        {
                            if (Math.Abs(i) < 0.001f) continue;
                            x.Add(i);
                            y.Add(MyF2(i));
                        }
                        plot.ShowAxis = true;
                        plot.SetParams(x, y, panel1.ClientRectangle);
                        plot.SetPenLine(new MyPen(DashStyle.DashDotDot, 3, Color.Red));
                        plot.SetPenAxis(new MyPen(DashStyle.Solid, 2, Color.Black));
                        plot.Draw(e.Graphics);
                        break;
                    }
                case "F3":
                    {
                        this.Width = 700;
                        this.Height = 700;
                        const float R = 3f;

                        const int N = 8;

                        for (int i = 0; i <= N; i++)
                        {
                            float angle = (float)(i * 2 * Math.PI / N);
                            x.Add((float)(R * Math.Cos(angle)));
                            y.Add((float)(R * Math.Sin(angle)));
                        }

                        plot.ShowAxis = false;
                        RectangleF fixedWorld = new RectangleF(-12f, -12f, 24f, 24f);
                        plot.SetParams(x, y, panel1.ClientRectangle, fixedWorld);
                        plot.SetPenLine(new MyPen(DashStyle.Solid, 3, Color.Red));
                        plot.SetPenAxis(new MyPen(DashStyle.Solid, 0));
                        plot.Draw(e.Graphics);
                        DrawCircle(e.Graphics, plot, R);
                        break;
                    }
            }
            e.Graphics.FillEllipse(Brushes.Aqua, 0, 0, 10, 10);
        }

        private void DrawCircle(Graphics graphics, CPlot2D plot, float R)
        {
            using (var penCircle = new Pen(Color.Blue, 2))
            using (var path = new GraphicsPath())
            {
                List<Point> points = new List<Point>();


                for (int angle = 0; angle <= 360; angle += 5)
                {
                    double rad = angle * Math.PI / 180;
                    double x1 = R * Math.Cos(rad);
                    double y1 = R * Math.Sin(rad);

                    plot.GetWindowCoords((float)x1, (float)y1, out int px, out int py);
                    points.Add(new Point(px, py));


                    if (angle <= 10)
                    {
                        Console.WriteLine($"Angle {angle}: world=({x1:F2}, {y1:F2}) -> screen=({px}, {py})");
                    }
                }


                if (points.Count > 1)
                {
                    path.AddLines(points.ToArray());
                    graphics.SmoothingMode = SmoothingMode.AntiAlias;
                    graphics.DrawPath(penCircle, path);
                }


            }
        }

        private float MyF1(float x) => (float)(Math.Sin(x) / x);
        private float MyF2(float x) => (float)(Math.Sqrt(Math.Abs(x)) * Math.Sin(x));

        private void F1(object sender, EventArgs e)
        {
            F = "F1";
            panel1.Invalidate();
        }

        private void F2(object sender, EventArgs e)
        {
            F = "F2";
            panel1.Invalidate();
        }

        private void F3(object sender, EventArgs e)
        {
            F = "F3";
            panel1.Invalidate();
        }
    }
}
