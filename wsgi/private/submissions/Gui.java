package oving_4;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.table.*;
import java.util.*;
import java.util.List;

/**
 * Graphical User Interface used by the servers
 * in a distributed transactional system.
 */
class Gui extends JFrame implements ActionListener
{
  /**
   * The maximum number of transaction tabs visible at any time
   */
  private static final int MAX_NOF_TABS = 10;
  /**
   * The output area used to display general output information
   */
  private OutputArea serverOutput;
  /**
   * The tabbed pane containing the output areas of the MAX_NOF_TABS most recent transactions
   */
  private JTabbedPane transactionPane;
  /**
   * Labels for displaying the number of aborted and committed transactions so far
   */
  private JLabel nofAbortsLabel;
  private JLabel nofCommitsLabel;
  /**
   * Data model used by the resource table
   */
  private ResourceTableModel resourceTableModel;
  /**
   * List displaying all known servers
   */
  private JList<String> serverList;
  /**
   * A reference to the server that this GUI belongs to
   */
  private ServerImpl server;
  /**
   * Button used to pause and resume the execution of transactions
   */
  private JButton pauseButton;
  /**
   * Whether or not the server is currently paused
   */
  private boolean pauseStatus = true;

  /**
   * Creates a new GUI.
   *
   * @param title     The title of the GUI window.
   * @param resources The resources hosted by this GUI's server.
   * @param servers   The servers known by this GUI's server.
   * @param server    The server that this GUI belongs to.
   * @param pos       Integer from 0-3 signifying which corner of the
   *                  screen to place the GUI in.
   */
  Gui(String title, List<Resource> resources, Map<Integer, Server> servers, ServerImpl server, int pos)
  {
    super(title);
    this.server = server;
    resourceTableModel = new ResourceTableModel(resources);
    serverList = new JList<String>();
    nofAbortsLabel = new JLabel();
    nofCommitsLabel = new JLabel();
    updateTransactionCounters(0, 0);
    updateServerList(servers);
    placeComponents();
    setSize(550, 450);
    setLocation((pos % 2) * 560, (pos / 2) * 460);
    setVisible(true);
    setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
  }

  /**
   * Gets the status indicated by the pause/continue button.
   *
   * @return Whether or not the arrival of new transactions has been halted by the user.
   */
  boolean getPauseStatus()
  {
    return pauseStatus;
  }

  /**
   * Updates the labels showing the number of aborted and committed transactions so far.
   *
   * @param nofAborts       The number of aborted transactions so far.
   * @param nofTransactions The number of executed transactions so far.
   */
  void updateTransactionCounters(int nofAborts, int nofTransactions)
  {
    nofAbortsLabel.setText("# of aborts so far: " + nofAborts);
    nofCommitsLabel.setText("# of commits so far: " + (nofTransactions - nofAborts));
  }

  /**
   * Updates the display of the table of resources.
   *
   * @param resources The resources located on this GUI's server.
   */
  void updateResourceTable(List<Resource> resources)
  {
    resourceTableModel.updateResourceList(resources);
  }

  /**
   * Updates the display of the list of online servers.
   *
   * @param servers The servers known to this GUI's server.
   */
  void updateServerList(Map<Integer, Server> servers)
  {
    Object[] integers = servers.keySet().toArray();
    Arrays.sort(integers);
    String names[] = new String[integers.length];
    for (int i = 0; i < integers.length; i++)
      names[i] = "Server " + integers[i];
    serverList.setListData(names);
  }

  /**
   * Creates and places the components of this GUI.
   */
  private void placeComponents()
  {
    serverOutput = new OutputArea("Server output:");
    transactionPane = new JTabbedPane();
    JTable resourceTable = new JTable(resourceTableModel);
    resourceTable.setCellSelectionEnabled(false);
    resourceTable.setColumnSelectionAllowed(false);
    resourceTable.setRowSelectionAllowed(false);
    serverList.setCellRenderer(new DefaultListCellRenderer()
    {
      public Component getListCellRendererComponent(JList list, Object value, int index, boolean isSelected, boolean cellHasFocus)
      {
        return super.getListCellRendererComponent(list, value, index, false, false);
      }
    });

    JPanel counterPanel = new JPanel(new GridLayout(2, 1));
    counterPanel.add(nofAbortsLabel);
    counterPanel.add(nofCommitsLabel);
    JPanel labelPanel = new JPanel(new GridLayout(1, 2));
    labelPanel.add(new JLabel("Most recent transactions:"));
    labelPanel.add(counterPanel);
    JPanel topPanel = new JPanel(new BorderLayout());
    pauseButton = new JButton("Start");
    pauseButton.addActionListener(this);
    topPanel.add(labelPanel, BorderLayout.CENTER);
    topPanel.add(pauseButton, BorderLayout.EAST);
    JPanel upperPanel = new JPanel(new BorderLayout());
    upperPanel.add(topPanel, BorderLayout.NORTH);
    upperPanel.add(transactionPane, BorderLayout.CENTER);
    JPanel serverPanel = new JPanel(new BorderLayout());
    JPanel resPanel = new JPanel(new BorderLayout());
    JPanel serversPanel = new JPanel(new BorderLayout());
    resPanel.add(new JLabel("Server resources:"), BorderLayout.NORTH);
    JScrollPane tableScrollPane = new JScrollPane(resourceTable);
    resourceTable.setPreferredScrollableViewportSize(new Dimension(150, 160));
    resPanel.add(tableScrollPane, BorderLayout.CENTER);
    serversPanel.add(new JLabel("Online servers:"), BorderLayout.NORTH);
    JScrollPane serverScrollPane = new JScrollPane(serverList);
    serversPanel.add(serverScrollPane, BorderLayout.CENTER);
    serverPanel.add(resPanel, BorderLayout.WEST);
    serverPanel.add(serverOutput, BorderLayout.CENTER);
    serverPanel.add(serversPanel, BorderLayout.EAST);

    Container cp = getContentPane();
    cp.setLayout(new BorderLayout());
    cp.add(upperPanel, BorderLayout.CENTER);
    cp.add(serverPanel, BorderLayout.SOUTH);
  }

  /**
   * Called whenever the start/pause/continue button is pressed.
   *
   * @param ae The ActionEvent that occured.
   */
  public void actionPerformed(ActionEvent ae)
  {
    if (ae.getSource() == pauseButton) {
      if (pauseButton.getText().equals("Start"))
        server.start();
      else {
        pauseStatus = !pauseStatus;
        pauseButton.setText(pauseStatus ? "Continue" : "Pause");
      }
    }
  }

  /**
   * Called by the server when another server has started up, and
   * asked this server to start as well.
   */
  void pressStartButton()
  {
    if (pauseButton.getText().equals("Start")) {
      pauseStatus = false;
      pauseButton.setText("Pause");
    }
  }

  /**
   * Creates an output area for a new transaction and adds it to the
   * tabbed pane. If this results in too many tabs, the oldest tab
   * is removed.
   *
   * @param transactionId The ID of the new transaction.
   */
  void newTransactionTab(int transactionId)
  {
    if (transactionPane.getTabCount() >= MAX_NOF_TABS)
      transactionPane.remove(0);
    OutputArea oa = new OutputArea("Output of transaction " + transactionId + ':');
    transactionPane.addTab(String.valueOf(transactionId), oa);
    transactionPane.setSelectedComponent(oa);
  }

  /**
   * Outputs a text string relevant to a specific transaction to that transaction's
   * output area, formated with a newline at the end.
   *
   * @param s   The information to display.
   * @param tId The ID of the transaction relevant to this information.
   */
  void println(String s, int tId)
  {
    print(s + '\n', tId);
  }

  /**
   * Outputs a text string relevant to a specific transaction to that transaction's
   * output area.
   *
   * @param s   The information to display.
   * @param tId The ID of the transaction relevant to this information.
   */
  void print(String s, int tId)
  {
    int index = transactionPane.indexOfTab(String.valueOf(tId));
    if (index > -1) {
      OutputArea oa = (OutputArea)transactionPane.getComponentAt(index);
      oa.print(s);
    }
  }

  /**
   * Outputs a text string with general information, formatted with a newline at the end.
   *
   * @param s The information to display.
   */
  void println(String s)
  {
    serverOutput.println(s);
  }

  /**
   * Outputs a text string with general information.
   *
   * @param s The information to display.
   */
  void print(String s)
  {
    serverOutput.print(s);
  }

  /**
   * Displays a dialog box with the given title and error message.
   *
   * @param title The title of the error dialog box.
   * @param error The error message displayed in the error dialog box.
   */
  void displayErrorMessage(String title, String error)
  {
    JOptionPane.showMessageDialog(this, error, title, JOptionPane.ERROR_MESSAGE);
  }

  /**
   * A component used to output textual information.
   */
  private static class OutputArea extends JPanel
  {
    /**
     * TextArea containing outputted information
     */
    private JTextArea textArea;

    /**
     * Creates a new output area.
     *
     * @param title The headline of the area.
     */
    OutputArea(String title)
    {
      JLabel headline = new JLabel(title);
      textArea = new JTextArea();
      setLayout(new BorderLayout());
      add(headline, BorderLayout.NORTH);
      add(new JScrollPane(textArea), BorderLayout.CENTER);
    }

    /**
     * Outputs a text string, with a newline added at the end, to this output area.
     *
     * @param s The information to display.
     */
    void println(String s)
    {
      print(s + '\n');
    }

    /**
     * Outputs a text string to this output area.
     *
     * @param s The information to display.
     */
    void print(String s)
    {
      textArea.append(s);
    }
  }

  /**
   * Data model specifying the contents of the
   * resource table in the GUI.
   */
  private static class ResourceTableModel extends AbstractTableModel
  {
    /**
     * The names of the columns in the table
     */
    private String columnNames[] = {"Resource", "Lock owner"};
    /**
     * The resources displayed in the table
     */
    private List<Resource> resources;

    /**
     * Creates a new resource table data model.
     *
     * @param resources The resources that the table should display.
     */
    ResourceTableModel(List<Resource> resources)
    {
      this.resources = resources;
    }

    /**
     * Updates the contents of this data model.
     *
     * @param resources The new list of resources to display.
     */
    void updateResourceList(List<Resource> resources)
    {
      this.resources = resources;
      fireTableDataChanged();
    }

    /**
     * Gets the name of the specified column.
     *
     * @param col The index of the column.
     * @return The name of the column with index col.
     */
    public String getColumnName(int col)
    {
      return columnNames[col];
    }

    /**
     * Gets the number of rows in the table.
     *
     * @return The number of resources in the table.
     */
    public int getRowCount()
    {
      return resources.size();
    }

    /**
     * Gets the number of columns in the table.
     *
     * @return The number of columns in the table.
     */
    public int getColumnCount()
    {
      return columnNames.length;
    }

    /**
     * Gets an object specifying the contents of the specified table cell.
     *
     * @param row The row index of the cell.
     * @param col The column index of the cell.
     * @return A string specifying the contents of the given cell.
     */
    public Object getValueAt(int row, int col)
    {
      if (col == 0)
        return String.valueOf(row);
      else if (col == 1) {
        int lockOwner = resources.get(row).getLockOwner();
        if (lockOwner == Resource.NOT_LOCKED)
          return "None";
        else
          return lockOwner;
      }
      else
        return "";
    }

    /**
     * Checks if a specified table cell is editable.
     *
     * @param row The row index of the cell.
     * @param col The column index of the cell.
     * @return Overridden to always return false.
     */
    public boolean isCellEditable(int row, int col)
    {
      return false;
    }
  }
}
