using System.Drawing;
using System.Windows.Forms;

namespace lab3
{
    partial class Form1
    {
        /// <summary>
        /// Обязательная переменная конструктора.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Освободить все используемые ресурсы.
        /// </summary>
        /// <param name="disposing">истинно, если управляемый ресурс должен быть удален; иначе ложно.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Код, автоматически созданный конструктором форм Windows

        /// <summary>
        /// Требуемый метод для поддержки конструктора — не изменяйте 
        /// содержимое этого метода с помощью редактора кода.
        /// </summary>
        private void InitializeComponent()
        {
            menuStrip1 = new MenuStrip();
            f1ToolStripMenuItem = new ToolStripMenuItem();
            tESTFF2ToolStripMenuItem = new ToolStripMenuItem();
            tESTFF3ToolStripMenuItem = new ToolStripMenuItem();
            panel1 = new Panel();
            menuStrip1.SuspendLayout();
            SuspendLayout();
            // 
            // menuStrip1
            // 
            menuStrip1.ImageScalingSize = new Size(20, 20);
            menuStrip1.Items.AddRange(new ToolStripItem[] { f1ToolStripMenuItem, tESTFF2ToolStripMenuItem, tESTFF3ToolStripMenuItem });
            menuStrip1.Location = new Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new Size(800, 28);
            menuStrip1.TabIndex = 0;
            menuStrip1.Text = "menuStrip1";
            // 
            // f1ToolStripMenuItem
            // 
            f1ToolStripMenuItem.Name = "f1ToolStripMenuItem";
            f1ToolStripMenuItem.Size = new Size(87, 24);
            f1ToolStripMenuItem.Text = "TESTF>F1";
            // 
            // tESTFF2ToolStripMenuItem
            // 
            tESTFF2ToolStripMenuItem.Name = "tESTFF2ToolStripMenuItem";
            tESTFF2ToolStripMenuItem.Size = new Size(87, 24);
            tESTFF2ToolStripMenuItem.Text = "TESTF>F2";
            // 
            // tESTFF3ToolStripMenuItem
            // 
            tESTFF3ToolStripMenuItem.Name = "tESTFF3ToolStripMenuItem";
            tESTFF3ToolStripMenuItem.Size = new Size(87, 24);
            tESTFF3ToolStripMenuItem.Text = "TESTF>F3";
            // 
            // panel1
            // 
            panel1.Location = new Point(0, 31);
            panel1.Name = "panel1";
            panel1.Size = new Size(800, 378);
            panel1.TabIndex = 1;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(panel1);
            Controls.Add(menuStrip1);
            Name = "Form1";
            Text = "Form1";
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion
        private MenuStrip menuStrip1;
        private ToolStripMenuItem f1ToolStripMenuItem;
        private ToolStripMenuItem tESTFF2ToolStripMenuItem;
        private ToolStripMenuItem tESTFF3ToolStripMenuItem;
        private Panel panel1;
    }
}

